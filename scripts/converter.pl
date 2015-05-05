use strict;
use warnings;
use utf8;
binmode(STDOUT, ":utf8");

use Data::Dumper;

use YAML::XS 'LoadFile';

use Template::Mustache;

sub get_original_games($)
{
	my $data = shift;
	
	my @return;
	
	# They are with name key:
	# name
	# [name, url wiki]
	
	# They are with names key:
	# [name, name]
	# [[name, url wiki], [name, url wiki]]
	
	foreach my $item (@{$data})
	{
		my $name = $item->{'name'};
		my $names = $item->{'names'};
		
		my $temp = undef;
		
		if (defined($name))
		{
			if (ref($name) eq "")
			{
				$temp->{'name'} = $name;
			}
			else
			{
				$temp->{'name'} = $name->[0];
			}
			
			push @return, $temp;
		}
		elsif (defined($names))
		{
			foreach my $name(@{$names})
			{
				$temp = undef;
				
				if (ref($name) eq "")
				{
					$temp->{'name'} = $name;
				}
				else
				{
					$temp->{'name'} = $name->[0];
				}
				
				push @return, $temp;
			}
		}
	}
	
	return \@return;
}



my $data = LoadFile('../games.yaml');
open FILE, "../template/template.md" or die "Couldn't open file: $!"; 
my $template = join("", <FILE>); 
close FILE;

my $json_data;

$json_data->{'original_games'} = get_original_games($data);

#~ print Dumper($json_data);

#~ print $template;


my $output = Template::Mustache::render(undef, $template, $json_data);

#~ print("\n\n");
#~ print($output);

open(my $fh, '>', '../README.md');
binmode($fh, ":utf8");
print $fh $output;
close $fh;