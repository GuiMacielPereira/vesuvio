"""Package defining entry points.
"""
import argparse
from os import environ, path
from EVSVesuvio.scripts import handle_config


def main():
    parser = __set_up_parser()
    args = parser.parse_args()
    if args.command == "config":
        __setup_config(args)

    if args.command == "run":
        if not handle_config.config_set():
            __setup_config(None)
        __run_analysis(args.yes)


def __set_up_parser():
    parser = argparse.ArgumentParser(description="Package to analyse Vesuvio instrument data")
    subparsers = parser.add_subparsers(dest='command', required=True)
    config_parser = subparsers.add_parser("config", help="set mvesuvio configuration")
    config_parser.add_argument("--set-cache", "-c", help="set the cache directory", default="", type=str)
    config_parser.add_argument("--set-ipfolder", "-p", help="set the intrument parameters directory", default="", type=str)
    config_parser.add_argument("--set-experiment", "-e", help="set the current experiment", default="", type=str)

    run_parser = subparsers.add_parser("run", help="run mvesuvio analysis")
    run_parser.add_argument("--yes", "-y", help="Say yes to all input prompts", action='store_true')
    return parser


def __setup_config(args):
    config_dir = handle_config.VESUVIO_CONFIG_PATH
    handle_config.setup_config_dir(config_dir)
    ipfolder_dir = handle_config.VESUVIO_IPFOLDER_PATH

    if handle_config.config_set():
        cache_dir = handle_config.read_config_var('caching.location') if not args or not args.set_cache else args.set_cache
        experiment = handle_config.read_config_var('caching.experiment') if not args or not args.set_experiment else args.set_experiment
        ipfolder_dir = handle_config.read_config_var('caching.ipfolder') if not args or not args.set_ipfolder else args.set_ipfolder
    else:
        cache_dir = config_dir if not args or not args.set_cache else args.set_cache
        experiment = "default" if not args or not args.set_experiment else args.set_experiment
        ipfolder_dir = ipfolder_dir if not args or not args.set_ipfolder else args.set_ipfolder

        handle_config.setup_default_ipfile_dir()

    handle_config.set_config_vars({'caching.location': cache_dir,
                                   'caching.experiment': experiment,
                                   'caching.ipfolder': ipfolder_dir})
    handle_config.setup_expr_dir(cache_dir, experiment)
    handle_config.check_dir_exists("IP folder", ipfolder_dir)


def __run_analysis(yes_to_all):
    environ['MANTIDPROPERTIES'] = path.join(handle_config.VESUVIO_CONFIG_PATH, "Mantid.user.properties")
    from EVSVesuvio import analysis_runner
    analysis_runner.run(yes_to_all)


if __name__ == '__main__':
    main()
