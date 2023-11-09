from dataclasses import dataclass, field
from typing import Dict, List, Union
import logging
_logger = logging.getLogger(__name__)



@dataclass
class FixedColumnWidthCSVGeneratorCol:
    format:str
    alignment:str
    fill:str
    width:int
    post_process_fn:callable

    @property
    def fill_format(self):
        return f"{{:{self.fill}{self.alignment}{self.width if not self.format else ''}{self.format}}}"

    def fill_value(self, value):
        return self.post_process_fn(self.fill_format.format(value)[:self.width])
    
@dataclass
class FixedColumnWidthCSVGenerator:
    columns: List[FixedColumnWidthCSVGeneratorCol] = field(default_factory=list)
    lines:List[str] = field(default_factory=list)
    column_separator:str = ''
    line_separator:str = '\n'

    def fill_columns(self, *args):
        return (col.fill_value(arg) for arg, col in zip(args, self.columns))

    def build_line(self, *args):
        
        return self.column_separator.join(self.fill_columns(*args))
    
    def add_line_with_args(self, *args):
        line = self.build_line(*args)
        self.add_line_with_str(line)

    def add_line_with_str(self, line):
        self.lines.append(line)

    def add_column(self, format, alignment, fill, width, post_process_fn):
        self.columns.append(FixedColumnWidthCSVGeneratorCol(format, alignment, fill, width, post_process_fn))

    def build(self):
        return self.line_separator.join(self.lines)
    
    def write_csv(self):
        with open('output.csv', 'w') as f:
            f.write(self.build())


