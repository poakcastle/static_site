from textnode import TextNode, TextType

def main():
    Dummy = TextNode("This is some anchor text", TextType.LINK, "https://www.boot.dev")
    print(Dummy)

main()