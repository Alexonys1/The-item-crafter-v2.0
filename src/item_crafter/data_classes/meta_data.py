class MetaData (type):
    def create_local_attrs(self, *args, **kwargs) -> None:
        self.__dict__.update(self.__class_attrs__)

    def __init__(cls, class_name, base_classes, attrs):
        cls.__class_attrs__ = attrs
        cls.__init__ = MetaData.create_local_attrs
