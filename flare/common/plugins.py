from functools import partial
from typing import Callable, Tuple, Union


def prepare_plugin(
    plugin_definition: Union[Callable, Tuple[Callable, Tuple]]
) -> Callable:
    if isinstance(plugin_definition, tuple):
        return partial(plugin_definition[0], **plugin_definition[1])
    else:
        return plugin_definition
