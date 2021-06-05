from mimetypes import types_map

from django.contrib.syndication.views import Feed
from django.utils import feedgenerator

from library.models import Book


class CustomSyndicationFeed(feedgenerator.Atom1Feed):
    """
    Custom feed type, modifying existing atom feed to opds purposes
    """
    mime_type = 'application/xml'
    content_type = "text/xml"

    def root_attributes(self):
        """
        adds attributes to root, such as namespaces
        :return:
        """
        attrs = super().root_attributes()
        attrs['xmlns'] = "http://www.w3.org/2005/Atom"
        attrs['xmlns:dc'] = "http://purl.org/dc/elements/1.1/"
        attrs['xmlns:opds'] = 'http://opds-spec.org/2010/catalog'
        return attrs

    def write_items(self, handler):
        """
        Set some elements that are the same across all items
        :param handler:
        :return:
        """
        for item in self.items:
            handler.startElement('entry', self.item_attributes(item))
            self.add_item_elements(handler, item)
            handler.endElement("entry")

    @staticmethod
    def _safe_add_element(handler, item, attr):
        """
        quick if element exists, add it
        :param handler:
        :param item:
        :param attr:
        :return:
        """
        if item.get(attr):
            handler.addQuickElement(attr, item[attr])

    def add_item_elements(self, handler, item):
        """
        add root elements of each entry
        :param handler:
        :param item:
        :return:
        """
        # Handle each element that needs to be added to an xml item
        # 'item' is a dict of attributes
        super().add_item_elements(handler, item)
        for author in item["authors"]:
            handler.startElement('author', self.item_attributes(item))
            handler.addQuickElement("name", author.sort)
            handler.addQuickElement("uri", f"CHANGEME/{author.id}")
            handler.endElement("author")
        for language in item["languages"]:
            handler.addQuickElement("dc:language", language.lang_code)
        for i in item["identifiers"]:
            handler.addQuickElement("dc:identifier", f"urn:{i.type}:{i.val}")

        handler.addQuickElement('issued', item["issued"])
        self._safe_add_element(handler, item, 'dc:publisher')
        handler.addQuickElement("link", "", {
            "rel": "CHANGEME/image",
            "href": item["cover"],
            "type": "image/jpeg"
        })
        handler.addQuickElement("link", "", {
            "rel": "CHANGEME/acquisition",
            "href": item["download"],
            "type": item["d_format"]
        })


class CustomFeed(Feed):
    """
    OPDS aquisition feed
    """
    feed_type = CustomSyndicationFeed

    title = 'Calibre library'
    link = '/opds3/'
    feed_guid = "CHANGEME"
    author_name = "Sagar Ramsaransing"
    author_link = "CHANGEME"

    def items(self):
        return Book.objects.all().order_by("id")

    def item_title(self, item: Book):
        return item.title

    def item_guid(self, obj: Book):
        return f"urn:uuid:{obj.id}"

    def item_updateddate(self, item: Book):
        return item.timestamp

    def item_enclosure_mime_type(self, item: Book):
        return types_map[f".{item.data_set.first().format.lower()}"]

    def item_copyright(self, book: Book):
        return f"Copyright (c) {book.pubdate.year}, {book.publisher}"

    def item_link(self, item: Book):
        return item.download_link

    def item_extra_kwargs(self, item: Book):
        """
        Fetch data that will be added for each entry
        :type item: Book
        """
        extra_kwargs = {
            "issued": item.pubdate.isoformat(),
            "authors": item.authors.all(),
            "languages": item.languages.all(),
            "identifiers": item.identifier_set.all(),
            "cover": item.cover_link,
            "download": item.download_link,
            "d_format": types_map.get(f".{item.data_set.first().format.lower()}", "application/octet-stream")
        }
        if item.publishers.all():
            extra_kwargs['dc:publisher'] = item.publisher.name
        return extra_kwargs

