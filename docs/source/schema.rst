Schema
!!!!!!


Overview
@@@@@@@@

.. _vr-schema-diagram:

.. figure:: images/schema-current.png

   Variation Representation Specfication (VRS) Schema Diagram

   VRS describes several classes for representing biological sequence
   variation.  Classes are shown as boxes. Inheritance and composition
   are shown with lines connecting classes.  Dashed borders denote
   abstract classes, which are not instantiated.  Four abstract
   classes -- :ref:`Variation`, :ref:`Location`, :ref:`State`, and
   :ref:`Interval` -- enable specializations of concepts in this and
   future versions of VRS.  Bold borders denote identifiable classes
   -- that may be referenced with an identifier.  Identifiable objects
   have an optional `_id` attribute.  Thin solid borders denote
   classes that not identifiable; these classes exist only to
   structure data within identifiable classes.  All classes have a
   string `type`.  Dashed arrow lines denote inheritance; subclasses
   inherit all attributes from their parent.  Inherited attributes are
   not shown in this diagram.  Solid lines with diamonds denote
   composition of one class with objects from another. An asterisk on
   a class attribute definition denotes an attribute that may contain
   either the object or a CURIE identifier to that object.


Machine Readable Specifications
@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

The machine readable VRS Specification is written using `JSON Schema
<https://json-schema.org/>`_.

The schema itself is written in YAML (|vr_yaml|) and converted to JSON
(|vr_json|).

Contributions to the schema MUST be written in the YAML document.
 
