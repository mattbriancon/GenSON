import argparse
import glob
import itertools
import json

from . import SchemaBuilder, __version__


def run(args: argparse.Namespace):
    builder = SchemaBuilder(schema_uri=args.schema_uri)

    for path in args.schema:
        with open(path, "r") as fp:
            builder.add_schema(json.load(fp))

    for path in itertools.chain(args.object, args.glob):
        with open(path, "r") as fp:
            builder.add_object(json.load(fp))

    print(builder.to_json(indent=args.indent))


def main():
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Generate one, unified JSON Schema from one or more JSON objects and/or JSON Schemas. Compatible with JSON-Schema Draft 4 and above.",
    )

    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )
    parser.add_argument(
        "--version",
        action="version",
        default=argparse.SUPPRESS,
        version="%(prog)s {}".format(__version__),
        help="Show version number and exit.",
    )
    parser.add_argument(
        "-i",
        "--indent",
        type=int,
        metavar="SPACES",
        help="Pretty-print the output, indenting SPACES spaces.",
    )
    parser.add_argument(
        "-s",
        "--schema",
        action="append",
        default=[],
        help="File containing a JSON Schema (can be specified multiple times to merge schemas).",
    )
    parser.add_argument(
        "-$",
        "--schema-uri",
        metavar="SCHEMA_URI",
        dest="schema_uri",
        default=SchemaBuilder.DEFAULT_URI,
        help=f"The value of the '$schema' keyword (defaults to {SchemaBuilder.DEFAULT_URI!r} or can be specified in a schema with the -s option). If {SchemaBuilder.NULL_URI!r} is passed, the '$schema' keyword will not be included in the result.",
    )
    parser.add_argument(
        "--glob",
        metavar="PATTERN",
        type=glob.iglob,
        help="lob pattern use to match files containing JSON objects",
    )
    parser.add_argument(
        "object",
        nargs=argparse.REMAINDER,
        help="Files containing JSON objects (defaults to stdin if no arguments are passed).",
    )

    run(parser.parse_args())


if __name__ == "__main__":
    main()
