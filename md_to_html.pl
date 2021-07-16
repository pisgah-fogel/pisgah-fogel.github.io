#!/usr/bin/perl

my $num_args = @ARGV;

sub format_hypertext {
	my $text = $_[0];
	$text =~ s/[ ]([^ ]+):\/\/([^ ]+)/ <a href=\"\1:\/\/\2\">\2<\/a>/g;
	return $text;
}

sub convert_file {
	my ($source, $destination) = @_;
	print("[v] $source -> $destination\n");
	my $status = sysopen(INPUTF, $source, O_RDONLY);
	if (not $status) {
		print("Error cannot read file $source\n");
		return;
	}
	$status = open(OUTPUTF, ">$destination");
	if (not $status) {
		print("Error write file $destination\n");
		close(INPUTF);
		return;
	}

	print(OUTPUTF "<!DOCTYPE html><meta charset=\"UTF-8\"><html><head><link rel=\"stylesheet\" href=\"styles.css\"></head><body id=\"main\"><div id=\"content\">");
	my $in_a_list = 0;
	my $in_a_code = 0;
	my $in_a_paragraph = 0;
	while (<INPUTF>) {
		my $line = $_;
		my $size = length($line);
		if ( $line =~ m/^```(.*)$/) {
			# TODO add $1 as title for the code block
			if ($in_a_list) {
				print(OUTPUTF "</ul>");
				$in_a_list = 0;
			}
			if ($in_a_paragraph) {
				print(OUTPUTF "</p>");
				$in_a_paragraph = 0;
			}
			if ($in_a_code) {
				print(OUTPUTF "</code></pre>");
				$in_a_code = 0;
			} else {
				print(OUTPUTF "<pre><code>");
				$in_a_code = 1;
			}
		}
		elsif ($in_a_code) {
			print(OUTPUTF "$line");
		}
		elsif ( $line eq "\n") {
			if ($in_a_paragraph) {
				print(OUTPUTF "</p>");
				$in_a_paragraph = 0;
			}
			if ($in_a_list) {
				print(OUTPUTF "</ul>");
				$in_a_list = 0;
			}
		}
		elsif ( $line =~ m/^#([^#].*)$/) {
			if ($in_a_list) {
				print(OUTPUTF "</ul>");
				$in_a_list = 0;
			}
			if ($in_a_paragraph) {
				print(OUTPUTF "</p>");
				$in_a_paragraph = 0;
			}
			print(OUTPUTF "<h1>$1</h1>");
		}
		elsif ( $line =~ m/^##([^#].*)$/) {
			if ($in_a_list) {
				print(OUTPUTF "</ul>");
				$in_a_list = 0;
			}
			if ($in_a_paragraph) {
				print(OUTPUTF "</p>");
				$in_a_paragraph = 0;
			}
			print(OUTPUTF "<h2>$1</h2>");
		}
		elsif ( $line =~ m/^###([^#].*)$/) {
			if ($in_a_list) {
				print(OUTPUTF "</ul>");
				$in_a_list = 0;
			}
			if ($in_a_paragraph) {
				print(OUTPUTF "</p>");
				$in_a_paragraph = 0;
			}
			print(OUTPUTF "<h3>$1</h3>");
		}
		elsif ( $line =~ m/^####(.*)$/) {
			if ($in_a_list) {
				print(OUTPUTF "</ul>");
				$in_a_list = 0;
			}
			if ($in_a_paragraph) {
				print(OUTPUTF "</p>");
				$in_a_paragraph = 0;
			}
			print(OUTPUTF "<h4>$1</h4>");
		}
		elsif ( $line =~ m/^[ ]?-[ ]*(.*)$/) {
			if (not $in_a_list) {
				$in_a_list = 1;
				print(OUTPUTF "<ul>");
			}
			$tmp = $1;
			$tmp = format_hypertext($tmp);
			print(OUTPUTF "<li>$tmp</li>");
		}
		else {
			if (not $in_a_paragraph) {
				print(OUTPUTF "<p>");
				$in_a_paragraph = 1;
			}
			$tmp = $line;
			$tmp = format_hypertext($tmp);
			print(OUTPUTF "$tmp<br />");
		}

	}

	print(OUTPUTF "</div></body></html>");
	close(OUTPUTF);
	close(INPUTF);
}

if ($num_args < 1) {
	print("Expect at least one argument: the markdown file to parse\n");
	exit(1);
}

foreach my $expr (@ARGV) {
	print(" - Looking at $expr\n");
	my @list = glob($expr);
	foreach my $file (@list) {
		print(" - Checking \"$file\"\n");
		if (-d $file) {
			# TODO explore the folder
		} elsif (-r $file and (-f $file or -l $file)) {
			if ( $file =~ m/^(.*)\.md$/ ) {
				my $html_file = "$1.html";
				convert_file($file, $html_file);
			} else {
				print("[w] Ignoring, this is not a markdown file\n");
			}
		}else {
			print("[x] File $file do not exist");
			exit(1);
		}

	}
}

#@files = 
