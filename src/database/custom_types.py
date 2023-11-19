from typing import Annotated, List

# Define custom annotations
bigint = Annotated[int, "big integer"]
bigint_array = Annotated[List[bigint], "list of big integers"]
