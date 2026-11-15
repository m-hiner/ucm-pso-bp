import argparse
import logging

from pso import pso_config, run
from pso.image import plot


def setup_logging(args: argparse.Namespace):
    log_level = logging.INFO
    log_fmt = '%(levelname)s\t%(message)s'
    if args.quiet:
        log_level = logging.FATAL
    if args.debug:
        log_level = logging.DEBUG
        log_fmt = '%(asctime)s\t' + log_fmt

    logging.basicConfig(level=log_level, format=log_fmt)

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="pso.py",
        description=(
            "Particle swarm optimization"
            " implementation for academic evaluation"
        ),
        epilog="Author: Martin Hiner"
    )
    parser.add_argument(
        "config",
        type=str,
        metavar="CONFIG_PATH",
        help="path to the input file"
    )
    parser.add_argument(
        "--variant",
        type=str,
        default="base",
        choices=[
            "base",
            "immediate"
        ],
        help="PSO variant to be used"
    )
    output_group = parser.add_mutually_exclusive_group()
    output_group.add_argument(
        "-i",
        "--image",
        type=str,
        metavar="PATH",
        help="output image path"
    )
    output_group.add_argument(
        "-r",
        "--raw",
        type=str,
        metavar="PATH",
        help="raw output file path"
    )
    verbosity_group = parser.add_mutually_exclusive_group()
    verbosity_group.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="do not print anything"
    )
    verbosity_group.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="print debug level logs"
    )

    return parser.parse_args()

def main():
    args = parse_args()
    setup_logging(args)
    pso_config.load(args.config)
    output = run(args.variant)
    
    if args.image:
        plot(output, pso_config, args.image)
        pso_config.log.info("Output saved to image \'%s\'", args.image)
    elif args.raw:
        with open(args.raw, "w") as fh:
            for x, y in output:
                fh.write(f"{x} {y}\n")
        pso_config.log.info("Output data save to file \'%s\'", args.raw)


if __name__ == "__main__":
    main()
