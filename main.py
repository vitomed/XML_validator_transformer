import os
import xmlschema
from functools import wraps
from lxml.etree import XMLSyntaxError, XSLT, parse
from xml.etree.ElementTree import ParseError
from xmlschema.exceptions import XMLSchemaKeyError
from xmlschema.validators.exceptions import XMLSchemaParseError

LOG = "log.txt"
XML = "file.xml"
XSD = "schema.xsd"
XSL = "style.xsl"
FILE = "resulting.xml"


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global log
        try:
            log.write(f"Call method {func.__name__}:  {args}, {kwargs}\n\n")
        except NameError:
            raise NameError(f"You must open a log file for recording")
        r = func(*args, **kwargs)
        log.write(f"{func.__name__} method is return: {r}\n\n")
        return r

    return wrapper


class Validator:

    def __init__(self, xsd_path: str, **kwargs):
        self.xsd_path = xsd_path
        super().__init__(**kwargs)

    @logger
    def validation(self, xml_path: str) -> [str, bool]:
        try:
            schema = xmlschema.XMLSchema(self.xsd_path)
            resp = schema.is_valid(xml_path)
        except ParseError as parser_exc:
            return f"File {os.path.basename(self.xsd_path)} schema is incorrectly composed: {parser_exc}"
        except XMLSchemaParseError as parser_err:
            return f"{os.path.basename(self.xsd_path)}, invalid schema syntax: {parser_err}"
        except XMLSchemaKeyError as key_exc:
            return f"{os.path.basename(xml_path)} does not match file schema: {key_exc}"
        return resp


class Transformer:

    def __init__(self, xsl_path: str, **kwargs):
        self.xsl_path = xsl_path
        super().__init__(**kwargs)

    @logger
    def transform(self, xlm_path: str, file: str) -> str:
        dom = parse(xlm_path)
        try:
            xsl_parse = parse(self.xsl_path)
        except XMLSyntaxError as syntax_exc:
            return f"Error in file syntax {os.path.basename(file)}: {syntax_exc}"
        transform = XSLT(xsl_parse)
        result = transform(dom)

        xsl_file = open(file, "wb")
        xsl_file.write(result)
        xsl_file.close()
        return "Success"


class Handler(Validator, Transformer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":
    log = open(f"{LOG}", "w")
    h = Handler(xsd_path=XSD, xsl_path=XSL)
    h.validation(xml_path=XML)
    h.transform(xlm_path=XML, file=FILE)
    h.validation(xml_path=FILE)
    log.close()
