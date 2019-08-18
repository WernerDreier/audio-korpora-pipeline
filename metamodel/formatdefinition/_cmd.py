# .\_cmd.py
# -*- coding: utf-8 -*-
# PyXB bindings for NM:af1bb962b498b5435efd04f5e613e2ff127b725a
# Generated 2019-08-17 21:06:04.818671 by PyXB version 1.2.7-DEV using Python 3.7.4.final.0
# Namespace http://www.clarin.eu/cmd/1 [xmlns:cmd]

from __future__ import unicode_literals
import pyxb
import pyxb.binding
import pyxb.binding.saxer
import io
import pyxb.utils.utility
import pyxb.utils.domutils
import sys
import pyxb.utils.six as _six
# Unique identifier for bindings created at the same time
_GenerationUID = pyxb.utils.utility.UniqueIdentifier('urn:uuid:0db06e22-c122-11e9-8ed7-9cb6d0d1638a')

# Version of PyXB used to generate the bindings
_PyXBVersion = '1.2.7-DEV'
# Generated bindings are not compatible across PyXB versions
if pyxb.__version__ != _PyXBVersion:
    raise pyxb.PyXBVersionError(_PyXBVersion)

# A holder for module-level binding classes so we can access them from
# inside class definitions where property names may conflict.
_module_typeBindings = pyxb.utils.utility.Object()

# Import bindings for namespaces imported into schema
import pyxb.binding.datatypes

# NOTE: All namespace declarations are reserved within the binding
Namespace = pyxb.namespace.NamespaceForURI('http://www.clarin.eu/cmd/1', create_if_missing=True)
Namespace.configureCategories(['typeBinding', 'elementBinding'])

def CreateFromDocument (xml_text, fallback_namespace=None, location_base=None, default_namespace=None):
    """Parse the given XML and use the document element to create a
    Python instance.

    @param xml_text An XML document.  This should be data (Python 2
    str or Python 3 bytes), or a text (Python 2 unicode or Python 3
    str) in the L{pyxb._InputEncoding} encoding.

    @keyword fallback_namespace An absent L{pyxb.Namespace} instance
    to use for unqualified names when there is no default namespace in
    scope.  If unspecified or C{None}, the namespace of the module
    containing this function will be used, if it is an absent
    namespace.

    @keyword location_base: An object to be recorded as the base of all
    L{pyxb.utils.utility.Location} instances associated with events and
    objects handled by the parser.  You might pass the URI from which
    the document was obtained.

    @keyword default_namespace An alias for @c fallback_namespace used
    in PyXB 1.1.4 through 1.2.6.  It behaved like a default namespace
    only for absent namespaces.
    """

    if pyxb.XMLStyle_saxer != pyxb._XMLStyle:
        dom = pyxb.utils.domutils.StringToDOM(xml_text)
        return CreateFromDOM(dom.documentElement)
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    saxer = pyxb.binding.saxer.make_parser(fallback_namespace=fallback_namespace, location_base=location_base)
    handler = saxer.getContentHandler()
    xmld = xml_text
    if isinstance(xmld, _six.text_type):
        xmld = xmld.encode(pyxb._InputEncoding)
    saxer.parse(io.BytesIO(xmld))
    instance = handler.rootObject()
    return instance

def CreateFromDOM (node, fallback_namespace=None, default_namespace=None):
    """Create a Python instance from the given DOM node.
    The node tag must correspond to an element declaration in this module.

    @deprecated: Forcing use of DOM interface is unnecessary; use L{CreateFromDocument}."""
    if fallback_namespace is None:
        fallback_namespace = default_namespace
    if fallback_namespace is None:
        fallback_namespace = Namespace.fallbackNamespace()
    return pyxb.binding.basis.element.AnyCreateFromDOM(node, fallback_namespace)


# Atomic simple type: {http://www.clarin.eu/cmd/1}Resourcetype_simple
class Resourcetype_simple (pyxb.binding.datatypes.string, pyxb.binding.basis.enumeration_mixin):

    """An atomic simple type."""

    _ExpandedName = pyxb.namespace.ExpandedName(Namespace, 'Resourcetype_simple')
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 8, 4)
    _Documentation = None
Resourcetype_simple._CF_enumeration = pyxb.binding.facets.CF_enumeration(value_datatype=Resourcetype_simple, enum_prefix=None)
Resourcetype_simple.Metadata = Resourcetype_simple._CF_enumeration.addEnumeration(unicode_value='Metadata', tag='Metadata')
Resourcetype_simple.Resource = Resourcetype_simple._CF_enumeration.addEnumeration(unicode_value='Resource', tag='Resource')
Resourcetype_simple.SearchService = Resourcetype_simple._CF_enumeration.addEnumeration(unicode_value='SearchService', tag='SearchService')
Resourcetype_simple.SearchPage = Resourcetype_simple._CF_enumeration.addEnumeration(unicode_value='SearchPage', tag='SearchPage')
Resourcetype_simple.LandingPage = Resourcetype_simple._CF_enumeration.addEnumeration(unicode_value='LandingPage', tag='LandingPage')
Resourcetype_simple._InitializeFacetMap(Resourcetype_simple._CF_enumeration)
Namespace.addCategoryObject('typeBinding', 'Resourcetype_simple', Resourcetype_simple)
_module_typeBindings.Resourcetype_simple = Resourcetype_simple

# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 39, 8)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}Header uses Python identifier Header
    __Header = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Header'), 'Header', '__httpwww_clarin_eucmd1_CTD_ANON_httpwww_clarin_eucmd1Header', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 42, 16), )

    
    Header = property(__Header.value, __Header.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}Resources uses Python identifier Resources
    __Resources = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Resources'), 'Resources', '__httpwww_clarin_eucmd1_CTD_ANON_httpwww_clarin_eucmd1Resources', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 94, 16), )

    
    Resources = property(__Resources.value, __Resources.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}IsPartOfList uses Python identifier IsPartOfList
    __IsPartOfList = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IsPartOfList'), 'IsPartOfList', '__httpwww_clarin_eucmd1_CTD_ANON_httpwww_clarin_eucmd1IsPartOfList', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 202, 16), )

    
    IsPartOfList = property(__IsPartOfList.value, __IsPartOfList.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}Components uses Python identifier Components
    __Components = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Components'), 'Components', '__httpwww_clarin_eucmd1_CTD_ANON_httpwww_clarin_eucmd1Components', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 218, 16), )

    
    Components = property(__Components.value, __Components.set, None, None)

    
    # Attribute CMDVersion uses Python identifier CMDVersion
    __CMDVersion = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'CMDVersion'), 'CMDVersion', '__httpwww_clarin_eucmd1_CTD_ANON_CMDVersion', pyxb.binding.datatypes.anySimpleType, fixed=True, unicode_default='1.2', required=True)
    __CMDVersion._DeclarationLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 228, 12)
    __CMDVersion._UseLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 228, 12)
    
    CMDVersion = property(__CMDVersion.value, __CMDVersion.set, None, None)

    _ElementMap.update({
        __Header.name() : __Header,
        __Resources.name() : __Resources,
        __IsPartOfList.name() : __IsPartOfList,
        __Components.name() : __Components
    })
    _AttributeMap.update({
        __CMDVersion.name() : __CMDVersion
    })
_module_typeBindings.CTD_ANON = CTD_ANON


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_ (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 43, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}MdCreator uses Python identifier MdCreator
    __MdCreator = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MdCreator'), 'MdCreator', '__httpwww_clarin_eucmd1_CTD_ANON__httpwww_clarin_eucmd1MdCreator', True, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 45, 28), )

    
    MdCreator = property(__MdCreator.value, __MdCreator.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}MdCreationDate uses Python identifier MdCreationDate
    __MdCreationDate = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MdCreationDate'), 'MdCreationDate', '__httpwww_clarin_eucmd1_CTD_ANON__httpwww_clarin_eucmd1MdCreationDate', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 54, 28), )

    
    MdCreationDate = property(__MdCreationDate.value, __MdCreationDate.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}MdSelfLink uses Python identifier MdSelfLink
    __MdSelfLink = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MdSelfLink'), 'MdSelfLink', '__httpwww_clarin_eucmd1_CTD_ANON__httpwww_clarin_eucmd1MdSelfLink', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 63, 28), )

    
    MdSelfLink = property(__MdSelfLink.value, __MdSelfLink.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}MdProfile uses Python identifier MdProfile
    __MdProfile = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MdProfile'), 'MdProfile', '__httpwww_clarin_eucmd1_CTD_ANON__httpwww_clarin_eucmd1MdProfile', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 72, 28), )

    
    MdProfile = property(__MdProfile.value, __MdProfile.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}MdCollectionDisplayName uses Python identifier MdCollectionDisplayName
    __MdCollectionDisplayName = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'MdCollectionDisplayName'), 'MdCollectionDisplayName', '__httpwww_clarin_eucmd1_CTD_ANON__httpwww_clarin_eucmd1MdCollectionDisplayName', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 81, 28), )

    
    MdCollectionDisplayName = property(__MdCollectionDisplayName.value, __MdCollectionDisplayName.set, None, None)

    _ElementMap.update({
        __MdCreator.name() : __MdCreator,
        __MdCreationDate.name() : __MdCreationDate,
        __MdSelfLink.name() : __MdSelfLink,
        __MdProfile.name() : __MdProfile,
        __MdCollectionDisplayName.name() : __MdCollectionDisplayName
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_ = CTD_ANON_


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_2 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 46, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_2 = CTD_ANON_2


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_3 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.date
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 55, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.date
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_3 = CTD_ANON_3


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_4 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.anyURI
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 64, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyURI
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_4 = CTD_ANON_4


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_5 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.anyURI
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 73, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyURI
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_5 = CTD_ANON_5


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_6 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 82, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_6 = CTD_ANON_6


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_7 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 95, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}ResourceProxyList uses Python identifier ResourceProxyList
    __ResourceProxyList = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResourceProxyList'), 'ResourceProxyList', '__httpwww_clarin_eucmd1_CTD_ANON_7_httpwww_clarin_eucmd1ResourceProxyList', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 97, 28), )

    
    ResourceProxyList = property(__ResourceProxyList.value, __ResourceProxyList.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}JournalFileProxyList uses Python identifier JournalFileProxyList
    __JournalFileProxyList = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'JournalFileProxyList'), 'JournalFileProxyList', '__httpwww_clarin_eucmd1_CTD_ANON_7_httpwww_clarin_eucmd1JournalFileProxyList', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 131, 28), )

    
    JournalFileProxyList = property(__JournalFileProxyList.value, __JournalFileProxyList.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}ResourceRelationList uses Python identifier ResourceRelationList
    __ResourceRelationList = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResourceRelationList'), 'ResourceRelationList', '__httpwww_clarin_eucmd1_CTD_ANON_7_httpwww_clarin_eucmd1ResourceRelationList', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 155, 28), )

    
    ResourceRelationList = property(__ResourceRelationList.value, __ResourceRelationList.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __ResourceProxyList.name() : __ResourceProxyList,
        __JournalFileProxyList.name() : __JournalFileProxyList,
        __ResourceRelationList.name() : __ResourceRelationList
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_7 = CTD_ANON_7


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_8 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 98, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}ResourceProxy uses Python identifier ResourceProxy
    __ResourceProxy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResourceProxy'), 'ResourceProxy', '__httpwww_clarin_eucmd1_CTD_ANON_8_httpwww_clarin_eucmd1ResourceProxy', True, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 100, 40), )

    
    ResourceProxy = property(__ResourceProxy.value, __ResourceProxy.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __ResourceProxy.name() : __ResourceProxy
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_8 = CTD_ANON_8


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_9 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 101, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}ResourceType uses Python identifier ResourceType
    __ResourceType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResourceType'), 'ResourceType', '__httpwww_clarin_eucmd1_CTD_ANON_9_httpwww_clarin_eucmd1ResourceType', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 103, 52), )

    
    ResourceType = property(__ResourceType.value, __ResourceType.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}ResourceRef uses Python identifier ResourceRef
    __ResourceRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResourceRef'), 'ResourceRef', '__httpwww_clarin_eucmd1_CTD_ANON_9_httpwww_clarin_eucmd1ResourceRef', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 113, 52), )

    
    ResourceRef = property(__ResourceRef.value, __ResourceRef.set, None, None)

    
    # Attribute id uses Python identifier id
    __id = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'id'), 'id', '__httpwww_clarin_eucmd1_CTD_ANON_9_id', pyxb.binding.datatypes.ID, required=True)
    __id._DeclarationLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 123, 48)
    __id._UseLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 123, 48)
    
    id = property(__id.value, __id.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __ResourceType.name() : __ResourceType,
        __ResourceRef.name() : __ResourceRef
    })
    _AttributeMap.update({
        __id.name() : __id
    })
_module_typeBindings.CTD_ANON_9 = CTD_ANON_9


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_10 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.anyURI
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 114, 56)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyURI
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_10 = CTD_ANON_10


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_11 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 132, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}JournalFileProxy uses Python identifier JournalFileProxy
    __JournalFileProxy = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'JournalFileProxy'), 'JournalFileProxy', '__httpwww_clarin_eucmd1_CTD_ANON_11_httpwww_clarin_eucmd1JournalFileProxy', True, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 134, 40), )

    
    JournalFileProxy = property(__JournalFileProxy.value, __JournalFileProxy.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __JournalFileProxy.name() : __JournalFileProxy
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_11 = CTD_ANON_11


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_12 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 135, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}JournalFileRef uses Python identifier JournalFileRef
    __JournalFileRef = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'JournalFileRef'), 'JournalFileRef', '__httpwww_clarin_eucmd1_CTD_ANON_12_httpwww_clarin_eucmd1JournalFileRef', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 137, 52), )

    
    JournalFileRef = property(__JournalFileRef.value, __JournalFileRef.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __JournalFileRef.name() : __JournalFileRef
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_12 = CTD_ANON_12


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_13 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.anyURI
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 138, 56)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyURI
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_13 = CTD_ANON_13


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_14 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 156, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}ResourceRelation uses Python identifier ResourceRelation
    __ResourceRelation = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'ResourceRelation'), 'ResourceRelation', '__httpwww_clarin_eucmd1_CTD_ANON_14_httpwww_clarin_eucmd1ResourceRelation', True, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 158, 40), )

    
    ResourceRelation = property(__ResourceRelation.value, __ResourceRelation.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __ResourceRelation.name() : __ResourceRelation
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_14 = CTD_ANON_14


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_15 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 159, 44)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}RelationType uses Python identifier RelationType
    __RelationType = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'RelationType'), 'RelationType', '__httpwww_clarin_eucmd1_CTD_ANON_15_httpwww_clarin_eucmd1RelationType', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 161, 52), )

    
    RelationType = property(__RelationType.value, __RelationType.set, None, None)

    
    # Element {http://www.clarin.eu/cmd/1}Resource uses Python identifier Resource
    __Resource = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Resource'), 'Resource', '__httpwww_clarin_eucmd1_CTD_ANON_15_httpwww_clarin_eucmd1Resource', True, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 171, 52), )

    
    Resource = property(__Resource.value, __Resource.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __RelationType.name() : __RelationType,
        __Resource.name() : __Resource
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_15 = CTD_ANON_15


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_16 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 162, 56)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute ConceptLink uses Python identifier ConceptLink
    __ConceptLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ConceptLink'), 'ConceptLink', '__httpwww_clarin_eucmd1_CTD_ANON_16_ConceptLink', pyxb.binding.datatypes.anyURI)
    __ConceptLink._DeclarationLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 165, 68)
    __ConceptLink._UseLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 165, 68)
    
    ConceptLink = property(__ConceptLink.value, __ConceptLink.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ConceptLink.name() : __ConceptLink
    })
_module_typeBindings.CTD_ANON_16 = CTD_ANON_16


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_17 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 172, 56)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}Role uses Python identifier Role
    __Role = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'Role'), 'Role', '__httpwww_clarin_eucmd1_CTD_ANON_17_httpwww_clarin_eucmd1Role', False, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 174, 64), )

    
    Role = property(__Role.value, __Role.set, None, None)

    
    # Attribute ref uses Python identifier ref
    __ref = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ref'), 'ref', '__httpwww_clarin_eucmd1_CTD_ANON_17_ref', pyxb.binding.datatypes.IDREF, required=True)
    __ref._DeclarationLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 185, 60)
    __ref._UseLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 185, 60)
    
    ref = property(__ref.value, __ref.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __Role.name() : __Role
    })
    _AttributeMap.update({
        __ref.name() : __ref
    })
_module_typeBindings.CTD_ANON_17 = CTD_ANON_17


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_18 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.string
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 175, 68)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.string
    
    # Attribute ConceptLink uses Python identifier ConceptLink
    __ConceptLink = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'ConceptLink'), 'ConceptLink', '__httpwww_clarin_eucmd1_CTD_ANON_18_ConceptLink', pyxb.binding.datatypes.anyURI)
    __ConceptLink._DeclarationLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 178, 80)
    __ConceptLink._UseLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 178, 80)
    
    ConceptLink = property(__ConceptLink.value, __ConceptLink.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __ConceptLink.name() : __ConceptLink
    })
_module_typeBindings.CTD_ANON_18 = CTD_ANON_18


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_19 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 203, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    
    # Element {http://www.clarin.eu/cmd/1}IsPartOf uses Python identifier IsPartOf
    __IsPartOf = pyxb.binding.content.ElementDeclaration(pyxb.namespace.ExpandedName(Namespace, 'IsPartOf'), 'IsPartOf', '__httpwww_clarin_eucmd1_CTD_ANON_19_httpwww_clarin_eucmd1IsPartOf', True, pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 205, 28), )

    
    IsPartOf = property(__IsPartOf.value, __IsPartOf.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        __IsPartOf.name() : __IsPartOf
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_19 = CTD_ANON_19


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_20 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = pyxb.binding.datatypes.anyURI
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 206, 32)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyURI
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_20 = CTD_ANON_20


# Complex type [anonymous] with content type ELEMENT_ONLY
class CTD_ANON_21 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type ELEMENT_ONLY"""
    _TypeDefinition = None
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_ELEMENT_ONLY
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 219, 20)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is pyxb.binding.datatypes.anyType
    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _HasWildcardElement = True
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        
    })
_module_typeBindings.CTD_ANON_21 = CTD_ANON_21


# Complex type [anonymous] with content type SIMPLE
class CTD_ANON_22 (pyxb.binding.basis.complexTypeDefinition):
    """Complex type [anonymous] with content type SIMPLE"""
    _TypeDefinition = Resourcetype_simple
    _ContentTypeTag = pyxb.binding.basis.complexTypeDefinition._CT_SIMPLE
    _Abstract = False
    _ExpandedName = None
    _XSDLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 104, 56)
    _ElementMap = {}
    _AttributeMap = {}
    # Base type is Resourcetype_simple
    
    # Attribute mimetype uses Python identifier mimetype
    __mimetype = pyxb.binding.content.AttributeUse(pyxb.namespace.ExpandedName(None, 'mimetype'), 'mimetype', '__httpwww_clarin_eucmd1_CTD_ANON_22_mimetype', pyxb.binding.datatypes.string)
    __mimetype._DeclarationLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 107, 68)
    __mimetype._UseLocation = pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 107, 68)
    
    mimetype = property(__mimetype.value, __mimetype.set, None, None)

    _AttributeWildcard = pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_lax, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1'))
    _ElementMap.update({
        
    })
    _AttributeMap.update({
        __mimetype.name() : __mimetype
    })
_module_typeBindings.CTD_ANON_22 = CTD_ANON_22


CMD = pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'CMD'), CTD_ANON, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 38, 4))
Namespace.addCategoryObject('elementBinding', CMD.name().localName(), CMD)



CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Header'), CTD_ANON_, scope=CTD_ANON, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 42, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Resources'), CTD_ANON_7, scope=CTD_ANON, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 94, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IsPartOfList'), CTD_ANON_19, scope=CTD_ANON, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 202, 16)))

CTD_ANON._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Components'), CTD_ANON_21, scope=CTD_ANON, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 218, 16)))

def _BuildAutomaton ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton
    del _BuildAutomaton
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 202, 16))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Header')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 42, 16))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Resources')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 94, 16))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IsPartOfList')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 202, 16))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Components')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 218, 16))
    st_3 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    transitions.append(fac.Transition(st_3, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    st_3._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON._Automaton = _BuildAutomaton()




CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MdCreator'), CTD_ANON_2, scope=CTD_ANON_, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 45, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MdCreationDate'), CTD_ANON_3, scope=CTD_ANON_, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 54, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MdSelfLink'), CTD_ANON_4, scope=CTD_ANON_, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 63, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MdProfile'), CTD_ANON_5, scope=CTD_ANON_, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 72, 28)))

CTD_ANON_._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'MdCollectionDisplayName'), CTD_ANON_6, scope=CTD_ANON_, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 81, 28)))

def _BuildAutomaton_ ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_
    del _BuildAutomaton_
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 45, 28))
    counters.add(cc_0)
    cc_1 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 54, 28))
    counters.add(cc_1)
    cc_2 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 63, 28))
    counters.add(cc_2)
    cc_3 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 81, 28))
    counters.add(cc_3)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MdCreator')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 45, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MdCreationDate')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 54, 28))
    st_1 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MdSelfLink')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 63, 28))
    st_2 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MdProfile')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 72, 28))
    st_3 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_3)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_3, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'MdCollectionDisplayName')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 81, 28))
    st_4 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_4)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_0, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_0, False) ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_1, True) ]))
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_1, False) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_1, False) ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
        fac.UpdateInstruction(cc_2, True) ]))
    transitions.append(fac.Transition(st_3, [
        fac.UpdateInstruction(cc_2, False) ]))
    st_2._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
         ]))
    st_3._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_4, [
        fac.UpdateInstruction(cc_3, True) ]))
    st_4._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_._Automaton = _BuildAutomaton_()




CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResourceProxyList'), CTD_ANON_8, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 97, 28)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'JournalFileProxyList'), CTD_ANON_11, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 131, 28)))

CTD_ANON_7._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResourceRelationList'), CTD_ANON_14, scope=CTD_ANON_7, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 155, 28)))

def _BuildAutomaton_2 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_2
    del _BuildAutomaton_2
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResourceProxyList')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 97, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'JournalFileProxyList')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 131, 28))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_7._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResourceRelationList')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 155, 28))
    st_2 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_2)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_2, [
         ]))
    st_1._set_transitionSet(transitions)
    transitions = []
    st_2._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_7._Automaton = _BuildAutomaton_2()




CTD_ANON_8._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResourceProxy'), CTD_ANON_9, scope=CTD_ANON_8, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 100, 40)))

def _BuildAutomaton_3 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_3
    del _BuildAutomaton_3
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 100, 40))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_8._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResourceProxy')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 100, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_8._Automaton = _BuildAutomaton_3()




CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResourceType'), CTD_ANON_22, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 103, 52)))

CTD_ANON_9._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResourceRef'), CTD_ANON_10, scope=CTD_ANON_9, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 113, 52)))

def _BuildAutomaton_4 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_4
    del _BuildAutomaton_4
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResourceType')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 103, 52))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_9._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResourceRef')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 113, 52))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_9._Automaton = _BuildAutomaton_4()




CTD_ANON_11._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'JournalFileProxy'), CTD_ANON_12, scope=CTD_ANON_11, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 134, 40)))

def _BuildAutomaton_5 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_5
    del _BuildAutomaton_5
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 134, 40))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_11._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'JournalFileProxy')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 134, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_11._Automaton = _BuildAutomaton_5()




CTD_ANON_12._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'JournalFileRef'), CTD_ANON_13, scope=CTD_ANON_12, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 137, 52)))

def _BuildAutomaton_6 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_6
    del _BuildAutomaton_6
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_12._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'JournalFileRef')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 137, 52))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_12._Automaton = _BuildAutomaton_6()




CTD_ANON_14._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'ResourceRelation'), CTD_ANON_15, scope=CTD_ANON_14, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 158, 40)))

def _BuildAutomaton_7 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_7
    del _BuildAutomaton_7
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 158, 40))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_14._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'ResourceRelation')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 158, 40))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_14._Automaton = _BuildAutomaton_7()




CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'RelationType'), CTD_ANON_16, scope=CTD_ANON_15, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 161, 52)))

CTD_ANON_15._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Resource'), CTD_ANON_17, scope=CTD_ANON_15, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 171, 52)))

def _BuildAutomaton_8 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_8
    del _BuildAutomaton_8
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=2, max=2, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 171, 52))
    counters.add(cc_0)
    states = []
    final_update = None
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'RelationType')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 161, 52))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_15._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Resource')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 171, 52))
    st_1 = fac.State(symbol, is_initial=False, final_update=final_update, is_unordered_catenation=False)
    states.append(st_1)
    transitions = []
    transitions.append(fac.Transition(st_1, [
         ]))
    st_0._set_transitionSet(transitions)
    transitions = []
    transitions.append(fac.Transition(st_1, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_1._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_15._Automaton = _BuildAutomaton_8()




CTD_ANON_17._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'Role'), CTD_ANON_18, scope=CTD_ANON_17, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 174, 64)))

def _BuildAutomaton_9 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_9
    del _BuildAutomaton_9
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=1, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 174, 64))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_17._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'Role')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 174, 64))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_17._Automaton = _BuildAutomaton_9()




CTD_ANON_19._AddElement(pyxb.binding.basis.element(pyxb.namespace.ExpandedName(Namespace, 'IsPartOf'), CTD_ANON_20, scope=CTD_ANON_19, location=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 205, 28)))

def _BuildAutomaton_10 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_10
    del _BuildAutomaton_10
    import pyxb.utils.fac as fac

    counters = set()
    cc_0 = fac.CounterCondition(min=0, max=None, metadata=pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 205, 28))
    counters.add(cc_0)
    states = []
    final_update = set()
    final_update.add(fac.UpdateInstruction(cc_0, False))
    symbol = pyxb.binding.content.ElementUse(CTD_ANON_19._UseForTag(pyxb.namespace.ExpandedName(Namespace, 'IsPartOf')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 205, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    transitions.append(fac.Transition(st_0, [
        fac.UpdateInstruction(cc_0, True) ]))
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, True, containing_state=None)
CTD_ANON_19._Automaton = _BuildAutomaton_10()




def _BuildAutomaton_11 ():
    # Remove this helper function from the namespace after it is invoked
    global _BuildAutomaton_11
    del _BuildAutomaton_11
    import pyxb.utils.fac as fac

    counters = set()
    states = []
    final_update = set()
    symbol = pyxb.binding.content.WildcardUse(pyxb.binding.content.Wildcard(process_contents=pyxb.binding.content.Wildcard.PC_strict, namespace_constraint=(pyxb.binding.content.Wildcard.NC_not, 'http://www.clarin.eu/cmd/1')), pyxb.utils.utility.Location('https://infra.clarin.eu/CMDI/1.x/xsd/cmd-envelop.xsd', 222, 28))
    st_0 = fac.State(symbol, is_initial=True, final_update=final_update, is_unordered_catenation=False)
    states.append(st_0)
    transitions = []
    st_0._set_transitionSet(transitions)
    return fac.Automaton(states, counters, False, containing_state=None)
CTD_ANON_21._Automaton = _BuildAutomaton_11()

