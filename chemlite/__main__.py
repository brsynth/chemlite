from rr_cache.rr_cache import (
    rrCache,
)
from rr_cache.Args import (
    build_args_parser
)
from logging import (
    Logger,
    getLogger
)
from colored import fg, bg, attr
from argparse import (
    ArgumentParser,
    Namespace
)
from json import dumps
from typing import (
    List,
    Dict,
    Tuple
)


def init(
    parser: 'ArgumentParser',
    args: 'Namespace'
) -> Logger:
    from brs_utils import create_logger
    from rr_cache._version import __version__

    if args.log.lower() in ['silent', 'quiet'] or args.silent:
        args.log = 'CRITICAL'

    if args.log.lower() in ['silent', 'quiet', 'def_info'] or args.silent:
        disable_rdkit_logging()
        # # Disable RDKIT logging
        # from rdkit import RDLogger
        # RDLogger.DisableLog('rdApp.*')


    # Create logger
    logger = create_logger(parser.prog, args.log)

    logger.info(
        '{color}{typo}rr_cache {version}{rst}{color}{rst}\n'.format(
            version = __version__,
            color=fg('white'),
            typo=attr('bold'),
            rst=attr('reset')
        )
    )
    logger.debug(args)

    return logger


def disable_rdkit_logging():
    """
    Disables RDKit whiny logging.
    """
    import rdkit.rdBase as rkrb
    import rdkit.RDLogger as rkl
    logger = rkl.logger()
    logger.setLevel(rkl.ERROR)
    rkrb.DisableLog('rdApp.error')


def entry_point():
    parser = build_args_parser(
        prog = 'rr_cache',
        description = 'RetroRules Cache'
    )
    args  = parser.parse_args()

    logger = init(parser, args)

    cache = rrCache(
        db=args.db,
        attrs=None,
        cache_dir=args.cache_dir,
        logger=logger
    )

    if args.gen_cache:
        rrCache.generate_cache(args.cache_dir, logger)
    elif args.reaction_rules is not None:
        print_attr(
            cache,
            'rr_reactions',
            args.reaction_rules,
            logger
        )
    elif args.reactions is not None:
        print_attr(
            cache,
            'template_reactions',
            args.reactions,
            logger
        )
    else:
        cache.load(args.attrs)


def print_attr(
    cache: 'rrCache',
    attr: str,
    attr_lst: List,
    logger: Logger = getLogger(__file__)
) -> None:
    cache.load([attr])
    if attr_lst == []:
        print(
            dumps(
                cache.get(attr),
                indent=4
            )
        )
    else:
        for id in attr_lst:
            try:
                print(
                    id+':',
                    dumps(
                        cache.get(attr)[id],
                        indent=4
                    )
                )
            except KeyError:
                logger.error(
                    'ID not found in rrCache(\'{attr}\'): {id}'.format(
                        attr=attr,
                        id=id
                    )
                )


if __name__ == '__main__':
    entry_point()
