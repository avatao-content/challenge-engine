import os
from glob import glob
from typing import Dict, Iterable, List, Tuple

from toolbox.config.docker import DOCKER_REGISTRY


def get_image_url(repo_name: str, repo_branch: str, short_name: str, absolute: bool = True) -> str:
    """
    Return an absolute docker image URL

    :param repo_name: name of the docker repository (challenge name)
    :param repo_branch: branch of the git repo (challenge version)
    :param short_name: [optional] e.g. solvable or controller
    :param absolute: [optional] return the absolute URL using the default registry?
    :return: absolute URL
    """
    if repo_branch != 'master':
        tag = '-'.join((short_name, repo_branch))
    else:
        tag = short_name

    image = ':'.join((repo_name, tag))

    if absolute:
        return '/'.join((DOCKER_REGISTRY, image))

    return image


def yield_dockerfiles(repo_path: str, repo_name: str, repo_branch: str, absolute: bool = True) -> Iterable[Tuple[str, str]]:
    """
    Yield (Dockerfile, image_url) pairs from the given repo_path

    :param repo_path: the repo path (parent of config.yml)
    :param repo_name: name of the docker repository (challenge name)
    :param absolute: [optional] yield absolute image URLs using the default registry?
    """
    for dockerfile in glob(os.path.join(repo_path, '*', 'Dockerfile')):
        short_name = os.path.basename(os.path.dirname(dockerfile))
        image = get_image_url(repo_name, repo_branch, short_name, absolute)
        yield dockerfile, image


def sorted_container_configs(containers: Dict[str, Dict]) -> List[Tuple[str, Dict]]:
    def sort_key(item: Tuple[str, Dict]):
        # The solvable must come first to share its volumes and namespaces
        if item[0] == "solvable":
            return 0
        # Then the controller if defined
        if item[0] == "controller":
            return 1
        # Then any other solvable in their current order
        return 2

    return sorted(containers.items(), key=sort_key)
