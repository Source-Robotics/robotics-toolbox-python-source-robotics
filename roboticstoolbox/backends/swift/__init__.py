# Lazy imports for optional swift dependency
try:
    from swift.SwiftRoute import SwiftServer, SwiftSocket, start_servers
    from swift.SwiftElement import SwiftElement, Slider, Select, \
        Checkbox, Radio, Button, Label
    from swift.Swift import Swift
except ImportError:
    # Stubs when swift is not installed
    Swift = None  # type: ignore
    SwiftServer = None  # type: ignore
    SwiftSocket = None  # type: ignore
    SwiftElement = None  # type: ignore
    Slider = None  # type: ignore
    Select = None  # type: ignore
    Checkbox = None  # type: ignore
    Radio = None  # type: ignore
    Button = None  # type: ignore
    Label = None  # type: ignore
    start_servers = None  # type: ignore


__all__ = [
    'Swift',
    'Slider',
    'SwiftElement',
    'Label',
    'Select',
    'Button',
    'Checkbox',
    'Radio',
    'SwiftServer',
    'SwiftSocket',
    'start_servers'
]
