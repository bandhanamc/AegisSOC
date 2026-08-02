from app.ai.parser.output_parser import OutputParser

sample = (
    "```yara\n"
    "rule Test\n"
    "{\n"
    "    meta:\n"
    "        author = \"AegisSOC\"\n"
    "\n"
    "    strings:\n"
    "        $a = \"powershell\"\n"
    "\n"
    "    condition:\n"
    "        $a\n"
    "}\n"
    "```"
)

print(OutputParser.clean(sample))