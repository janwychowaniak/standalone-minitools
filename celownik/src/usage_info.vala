void usage() {
	string usage_str = "Cels' manager ;).\n";
	usage_str += "Possible args:\n";
	usage_str +="-l\t\t\t- list cels\n";
	usage_str +="-d [nr]\t\t\t- delete cel of nr\n";
	usage_str +="-a [YYYY-MM-DD] \"text\"\t- add cel\n";
	usage_str += "\nEnjoy the era ov ultra-productivity.";
	stdout.printf("%s\n", usage_str);
}
