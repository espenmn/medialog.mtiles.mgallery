from plone.app.standardtiles.contentlisting import ContentListingTile, DefaultQuery as baseDefaultQuery, DefaultSortOn as baseDefaultSortOn
from plone.app.z3cform.widget import QueryStringFieldWidget
from plone.autoform.directives import widget
from zope.interface import implementer
from zope.component import adapter
from plone.app.imaging.interfaces import IImageScaling
from plone.supermodel import model
from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from z3c.form.interfaces import IValue
from z3c.form.util import getSpecification
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from zope.component import queryUtility, getMultiAdapter, queryMultiAdapter
from zope.publisher.browser import BrowserView
from zope.schema import getFields
from zope import schema
from plone.tiles import Tile
from plone.tiles.interfaces import ITileType
from medialog.mtiles.mgallery import _
from Products.CMFPlone import PloneMessageFactory as _pmf

class IMgalleryTile(model.Schema):
    """M Gallery Tile schema"""

    widget(query=QueryStringFieldWidget)
    query = schema.List(
        title=_(u"Search terms"),
        value_type=schema.Dict(value_type=schema.Field(),
                               key_type=schema.TextLine()),
        description=_(u"Define the search terms for the items "
                      u"you want to list by choosing what to match on. The "
                      u"list of results will be dynamically updated"),
        required=False
    )

    sort_on = schema.TextLine(
        title=_(u'label_sort_on', default=u'Sort on'),
        description=_(u"Sort the collection on this index"),
        required=False,
    )

    sort_reversed = schema.Bool(
        title=_(u'label_sort_reversed', default=u'Reversed order'),
        description=_(u'Sort the results in reversed order'),
        required=False,
    )

    limit = schema.Int(
        title=_(u'Limit'),
        description=_(u'Limit Search Results'),
        required=False,
        default=100,
        min=1,
    )
    
    maxwidth = schema.Int(
        title=_(u'Max width'),
        required=True,
        default=1440,
        min=500,
    )
    
    speed = schema.Int(
        title=_(u'Speed'),
        required=True,
        default=500,
        min=10,
    )
    
    
    timeout = schema.Int(
        title=_(u'Speed'),
        required=True,
        default=1500,
        min=10,
    )
    
@implementer(IValue)
@adapter(None, None, None, getSpecification(IMgalleryTile['query']), None)  # noqa
class DefaultQuery(baseDefaultQuery):
    """Default Query"""
    
@implementer(IValue)
@adapter(None, None, None, getSpecification(IMgalleryTile['sort_on']), None)  # noqa
class DefaultSortOn(baseDefaultSortOn):
    """Default Sort On"""

def jsbool(val):
    if val:
        return 'true'
    return 'false'

class MgalleryTile(Tile):
    """M Gallery Tile"""

    slidertypes = ['default', 'compact', 'grid', 'slider']
    staticFilesRelative = '++resource++medialog.mtiles.mgallery'

    def __init__(self, context, request):
        super(MgalleryTile, self).__init__(context, request)
        portal_state = getMultiAdapter((context, request),
                                        name='plone_portal_state')
        self.portal_url = portal_state.portal_url()
        self.staticFiles = "%s/%s" % (self.portal_url,
                                      self.staticFilesRelative)


    @property
    def data(self):
        data = super(MgalleryTile, self).data
        if data.get('custom_options'):
            data.update(dict([(k,v) for k,v in [line.split(':') for line in data.get('custom_options').split(',') if line]]))
        return data
        
    def getUID(self):
        return self.request.get('URL').split('/')[-1]

    @property
    def maxwidth(self):
        return self.data.get('maxwidth', '')
    
    @property
    def speed(self):
        return self.data.get('speed', '')

    @property
    def timeout(self):
        return self.data.get('timeout', '')

    
    def script(self):
        return " "


    def tag(self, img, fieldname=None, scale=None, height=None, width=None,
            css_class=None, direction='keep', data={}, **args):

        if scale is not None:
            available = self.getAvailableSizes(fieldname)
            if scale not in available:
                return None
            width, height = available[scale]

        if width is None and height is None:
            field = self.field(fieldname)
            return field.tag(
                self.context, css_class=css_class, **args
            )

        info = self.getInfo(
            fieldname=fieldname, scale=scale,
            height=height, width=width,
            direction=direction,
        )

        width = info['width']
        height = info['height']
        mimetype = info['mimetype']
        extension = mimetype.split('/')[-1]

        url = self.context.absolute_url()
        src = '%s/@@images/%s.%s' % (url, info['uid'], extension)
        result = '<img src="%s"' % src

        if height:
            result = '%s height="%s"' % (result, height)

        if width:
            result = '%s width="%s"' % (result, width)

        if css_class is not None:
            result = '%s class="%s"' % (result, css_class)

        if data:
            for key, value in sorted(data.items()):
                if value:
                    result = '%s %s="%s"' % (result, key, value)
        if args:
            for key, value in sorted(args.items()):
                if value:
                    result = '%s %s="%s"' % (result, key, value)

        return '%s />' % result

    def contents(self):
        self.query = self.data.get('query')
        self.sort_on = self.data.get('sort_on')

        if self.query is None or self.sort_on is None:
            # Get defaults
            tileType = queryUtility(ITileType, name=self.__name__)
            fields = getFields(tileType.schema)
            if self.query is None:
                self.query = getMultiAdapter((
                    self.context,
                    self.request,
                    None,
                    fields['query'],
                    None
                ), name="default").get()
            if self.sort_on is None:
                self.sort_on = getMultiAdapter((
                    self.context,
                    self.request,
                    None,
                    fields['sort_on'],
                    None
                ), name="default").get()

        self.limit = self.data.get('limit')
        if self.data.get('sort_reversed'):
            self.sort_order = 'reverse'
        else:
            self.sort_order = 'ascending'
        """Search results"""
        builder = getMultiAdapter(
            (self.context, self.request), name='querybuilderresults'
        )
        accessor = builder(
            query=self.query,
            sort_on=self.sort_on or 'getObjPositionInParent',
            sort_order=self.sort_order,
            limit=self.limit
        )
        return accessor

    def tags(self):
        out = []
        for item in self.contents():
            img = item.getObject()
            image = queryMultiAdapter((img, self.request), name='images', default=None)
            if not image:
                continue
            data = {'data-title':item.Title().decode('utf-8'),
                    'data-description':item.Description().decode('utf-8'),
                    'data-image':item.getURL()}
            try:
                tag = image.tag(scale='preview')[:-2]
            except:
                continue
            for key, value in sorted(data.items()):
                if value:
                    tag = '%s %s="%s"' % (tag, key, value)
            tag = '%s />' % tag
            out.append(tag)
        return out

