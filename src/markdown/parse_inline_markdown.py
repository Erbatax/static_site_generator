import re
from node.textnode import TextNode, TextType


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        split_nodes = node.text.split(delimiter)

        if len(split_nodes) % 2 != 1:
            raise Exception("Unbalanced delimiter")

        for i in range(len(split_nodes)):
            split_node = split_nodes[i]
            if split_node == "":
                continue
            if i % 2 == 0:
                new_node = TextNode(split_node, node.text_type)
                new_nodes.append(new_node)
            else:
                new_node = TextNode(split_node, text_type)
                new_nodes.append(new_node)
    return new_nodes


def extract_markdown_images(text):
    # image in markdown ![alt text](url)
    return re.findall(r"\!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    # link in markdown [text](url)
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_images(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        images = extract_markdown_images(node.text)
        if len(images) == 0:
            new_nodes.append(node)
            continue

        text = node.text
        for image in images:
            image_alt = image[0]
            image_link = image[1]
            sections = text.split(f"![{image_alt}]({image_link})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], node.text_type))
            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_link))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, node.text_type))

    return new_nodes


def split_nodes_links(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue

        links = extract_markdown_links(node.text)

        text = node.text
        for link in links:
            link_text = link[0]
            link_url = link[1]
            sections = text.split(f"[{link_text}]({link_url})", 1)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], node.text_type))
            new_nodes.append(TextNode(link_text, TextType.LINK, link_url))
            text = sections[1]
        if text != "":
            new_nodes.append(TextNode(text, node.text_type))

    return new_nodes


def text_to_textnodes(text):
    all_nodes = []
    for line in text.split("\n"):
        nodes = [TextNode(line.strip(), TextType.TEXT)]
        nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
        nodes = split_nodes_delimiter(nodes, "*", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
        nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        nodes = split_nodes_links(nodes)
        nodes = split_nodes_images(nodes)
        all_nodes.extend(nodes)
        all_nodes.append(TextNode("\n", TextType.TEXT))
    return all_nodes[:-1]
