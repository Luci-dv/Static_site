class HTMLNode():
    def __init__(self, tag = None, value = None, children = None, props = None):
        self.tag = tag
        self.value = value
        if children is not None:
            self.children = children
        else:
            self.children = []
        if props is not None:
            self.props = props
        else:
            self.props = {}
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        current_string = ""
        if self.props:
            for key in self.props:
                current_string = current_string + " " + key + f'="{self.props[key]}"'
        return current_string
    
    def __eq__(self, other):
        return (
            self.tag == other.tag and
            self.value == other.value and
            self.children == other.children and
            self.props == other.props
        )
    
    def __repr__(self):
        return f"tag = {self.tag}, value = {self.value}, children = {self.children}, props = {self.props}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props = None):
        if value is None:
            raise ValueError("LeafNode must have a value")
        super().__init__(tag, value, children = None, props = props)

    def to_html(self):
        if self.tag is None:
            return self.value
        else:
            html = f"<{self.tag}"
            if self.props:
                for prop, value in self.props.items():
                    html += f' {prop}="{value}"'
            html += f">{self.value}</{self.tag}>"
            return html

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props = None):
        super().__init__(tag, value = None, children = children, props = props)
    
    def to_html(self):
        if self.tag is None:
            raise ValueError("Parent Node must have a Tag")
        if self.children is None or len(self.children) == 0:
            raise ValueError("Parent Node must have child nodes")
        if self.props:
            props_str = " " + " ".join([f'{key}="{value}"' for key, value in self.props.items()])
            current_string = f"<{self.tag}{props_str}>"
        else:
            current_string = f"<{self.tag}>"
        for obj in self.children:
            current_string += obj.to_html()
        current_string += f"</{self.tag}>"
        return current_string