RESTful Object-Oriented JSON (rooj, like huge)
==============================================

What is it
----------

HTML works well as the standard RESTful medium for humans. It uses a shared vocabulary understood by web browsers and servers that can display pages to humans who can then make hypertext navigation decisions based on inbuilt human readable cues (such as the text content of an anchor element).

But HTML is a bad choice for building a RESTful computer to computer interface. JSON is a good choice. However, unlike with HTML, there is no generally accepted vocabulary for JSON, meaning web application developers tend to roll their own each time. Rather than propose a new vocabulary, which would be unlikely to be sufficiently flexible for everyone's needs, rooj provides a structure to build JSON vocabularies easily, that can readily be extended, understood at a glance by developers, and

A RESTful API in essence serves a self-discoverable resource graph. A natural implementation by a client or server running an object-oriented runtime would be to represent this graph using a class-based object graph, with a class to represent each resource type. Rooj provides the framework to do this.

Examples
--------

Python
******

Usage::

    from rooj import Roojable


    class Person(Roojable):
        def __init__(self, first_name=None, last_name=None):
            self.first_name = first_name
            self.last_name = last_name


    class Root(Roojable):

        def __init__(self):
            self.attribute_1 = 5
            self.attribute_2 = "value"
            self.people = []

        def add_person(self, person):


    root = Root()
    root.people.append(Person(first_name="Alice", last_name="Ace"))
    root.to_rooj()

    people = root.rooj_get("people")
    person = root.rooj_get("people/0")
    person = root.rooj_post("people", "{}")

    {
        "_rooj_self": "/",
        "_rooj_class": "Root",
        "attribute_1": 5,
        "attribute_2": "value",
        "people": {}
    }
    {
        "_rooj_self": "/",
        "_rooj_class": "Root",
        "attribute_1": 5,
        "attribute_2": "value"
        "people": {
            "_rooj_class": "RoojList",
            "_rooj_url": "people",
            "_rooj_actions": {
                "post": {
                    "_rooj_classes": [
                        "Person"
                    ]
                }
            },
            "length": 1
        }
    }


