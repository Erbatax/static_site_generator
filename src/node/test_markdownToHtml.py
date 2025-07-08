import unittest

from node.markdownToHtmlNode import markdown_to_html_node


class TestMarkdownToHtml(unittest.TestCase):

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with _italic_ text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph\ntext in a p\ntag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_codeblock(self):
        md = """
```
This is text that _should_ remain
the **same** even with inline stuff
```
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><pre><code>This is text that _should_ remain\nthe **same** even with inline stuff\n</code></pre></div>",
        )

    def test_quotes(self):
        md = """    
> This is a quote
> This is a second quote
> This is a third quote
"""

        node = markdown_to_html_node(md)
        print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote\nThis is a second quote\nThis is a third quote</blockquote></div>",
        )

    def test_real_quotes(self):
        md = """
Here's the deal, **I like Tolkien**.

> "I am in fact a Hobbit in all but size."
>
> -- J.R.R. Tolkien
"""

        node = markdown_to_html_node(md)
        print(node)
        html = node.to_html()
        self.assertEqual(
            html,
            '<div><p>Here\'s the deal, <b>I like Tolkien</b>.</p><blockquote>"I am in fact a Hobbit in all but size."\n\n-- J.R.R. Tolkien</blockquote></div>',
        )


if __name__ == "__main__":
    unittest.main()
