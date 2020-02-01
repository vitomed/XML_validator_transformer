import os
import xmlschema
from functools import wraps
from lxml.etree import XMLSyntaxError, XSLT, parse
from xmlschema.exceptions import XMLSchemaKeyError
from xml.etree.ElementTree import ParseError

LOG = "log.txt"
PATH_XML = "file.xml"
PATH_XSD = "schema.xsd"
PATH_XSLT = "style.xsl"
RESULT_FILE = "resulting.xml"


def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        global log
        try:
            log.write(f"Call method {func.__name__}, {args}, {kwargs}\n\n")
        except NameError:
            raise NameError(f"You must open a log file for recording")
        r = func(*args, **kwargs)
        log.write(f"{func.__name__} method is return, {r}\n\n")
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
        except XMLSchemaKeyError as key_exc:
            return f"{os.path.basename(xml_path)} does not match file schema: {key_exc}"
        return resp


class Transformer:

    def __init__(self, xslt_path: str, **kwargs):
        self.xslt_path = xslt_path
        super().__init__(**kwargs)

    @logger
    def transform(self, xlm_path: str, result_file: str) -> [None, str]:
        dom = parse(xlm_path)
        try:
            xslt = parse(self.xslt_path)
        except XMLSyntaxError as exc:
            return f"Error in file syntax {os.path.basename(result_file)}: {exc}"
        transform = XSLT(xslt)
        result = transform(dom)
        xsl_file = open(result_file, "wb")
        xsl_file.write(result)
        xsl_file.close()
        return "Success"


class Handler(Validator, Transformer):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)


if __name__ == "__main__":
    log = open(f"{LOG}", "w")
    h = Handler(xsd_path=PATH_XSD, xslt_path=PATH_XSLT)
    h.validation(xml_path=PATH_XML)
    h.transform(xlm_path=PATH_XML, result_file=RESULT_FILE)
    h.validation(xml_path=RESULT_FILE)
    log.close()
