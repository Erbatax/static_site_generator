class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = (
            children if children is None or isinstance(children, list) else [children]
        )
        self.props = props

    def to_html(self):
        return f"<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>"

    def props_to_html(self):
        if self.props is None:
            return ""
        return "".join([f' {key}="{value}"' for key, value in self.props.items()])

    def __eq__(self, value):
        if not isinstance(value, HTMLNode):
            return False
        return (
            self.tag == value.tag
            and self.value == value.value
            and self.children == value.children
            and self.props == value.props
        )

    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
