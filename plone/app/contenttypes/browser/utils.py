# -*- coding: utf-8 -*-
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from Products.MimetypesRegistry.MimeTypeItem import guess_icon_path
from plone.memoize.view import memoize
from zope.component import getMultiAdapter
from zope.interface import Interface
from zope.interface import implements


class IUtils(Interface):
    """
    """

    def getMimeTypeIcon(content_file):
        """

        """


class Utils(BrowserView):
    implements(IUtils)

    @memoize
    def getMimeTypeIcon(self, content_file):
        context = aq_inner(self.context)
        pstate = getMultiAdapter(
            (context, self.request),
            name=u'plone_portal_state'
        )
        portal_url = pstate.portal_url()
        mtr = getToolByName(context, "mimetypes_registry")
        mime = list(mtr.lookup(content_file.contentType))
        mime.append(mtr.lookupExtension(content_file.filename))
        mime.append(mtr.lookup("application/octet-stream")[0])
        icon_paths = [m.icon_path for m in mime if hasattr(m, 'icon_path')]
        if icon_paths:
            return icon_paths[0]

        return portal_url + "/" + guess_icon_path(mime[0])

        # function works but is possibly not best implementation. following
        # code might work for files where the mimetype is not directly
        # recognized

#        if len(mime) > 0:
#            icon = portal_url + "/" + guess_icon_path(mime[0])
#        else:
#            mime = mtr.lookupExtension(content_file.filename)
#            if mime <> "":
#                icon = portal_url + "/" + guess_icon_path(mime)
#            else:
#                logger.info(
#                   "No MimeType Icon found for MimeType: " + \
#                   str(content_file.contentType)
#                   )
#                icon = portal_url + "/application.png"
#        return icon
