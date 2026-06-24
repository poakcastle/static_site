class HTMLNode():
    def __init__(
            self, 
            tag: str | None = None, 
            value: str | None = None,
            children: list["HTMLNode"] | None = None,
            props: dict[str, str] | None = None,
        ) -> None:
        
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("Error: to_html method not implemented")
    
    def props_to_html(self):
        if self.props is None:
            return ""
        for key in self.props:
            return f' {key}="{self.props[key]}"'
    
    def __repr__(self) -> str:
        return f"HTMLNode(tag={self.tag}, value={self.value}, children={self.children}, props={self.props})"

class LeafNode(HTMLNode):
    def __init__(
            self,
            tag: str, 
            value: str,  
            props: dict[str, str] | None = None
        ) -> None:

        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Error: leaf node must have a 'value'")
        elif self.tag is None:
            return self.value
        else:
            return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
    
    def __repr__(self) -> str:
        return f"LeafNode(tag={self.tag}, value={self.value}, props={self.props})"

class ParentNode(HTMLNode):
    def __init__(
            self,
            tag: str, 
            children: list["HTMLNode"], 
            props: dict[str, str] | None = None,
        ) -> None:

        super().__init__(tag, None, children, props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Error: parent node must have a 'tag'")
        elif self.children is None or len(self.children) == 0:
            raise ValueError("Error: parent node must have 'children'")
        else:
            html_string = f'<{self.tag}{self.props_to_html()}>'
            for child in self.children:
                html_string += f'{child.to_html()}'
            html_string += f'</{self.tag}>'
            return html_string
        