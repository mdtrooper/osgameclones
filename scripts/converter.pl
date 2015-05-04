use strict;
use warnings;
use utf8;
binmode(STDOUT, ":utf8");

use Data::Dumper;

use YAML::XS 'LoadFile';

use lib "Template";
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
		
		if (defined($name))
		{
			if (ref($name) eq "")
			{
				push @return, $name;
			}
			else
			{
				push @return, $name->[0];
			}
		}
		elsif (defined($names))
		{
			foreach my $name(@{$names})
			{
				if (ref($name) eq "")
				{
					push @return, $name;
				}
				else
				{
					push @return, $name->[0];
				}
			}
		}
	}
	
	return \@return;
}



my $test = LoadFile('../games.yaml');

my $json_data;

$json_data->{'original_games'} = get_original_games($test);
#~ 
#~ print Dumper($json_data);

my %test;
$test{'caca'} = 666;
print Template::Mustache.render("pedo");
