# Class for automated `__repr__`
class PrettyRepr:
    def __repr__(self) -> str:
        return "<{}({})>".format(
            f"{self.__class__.__name__} (object id {id(self.__class__)})",
            ", ".join(
                f"{attr}={repr(getattr(self, attr))}"
                for attr in filter(lambda x: not x.startswith("_"), self.__dict__)
            ),
        )
