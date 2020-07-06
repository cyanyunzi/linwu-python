import os

from mako.template import Template

from utils import DBUtils
# 初始化数据库
from utils import StringUtils


# 表对象
class Table:
    fields = []
    comment = ""
    name = ""
    className = ""
    author = ""
    basePackage = ""
    package = ""
    imports = []


# 字段对象
class Field:
    PRI_KEY = "PRI"
    name = ""
    type = ""
    javaType = ""
    javaName = ""
    comment = ""
    isPri = False
    culumn_constant = ""
    field_constant = ""
    valid = ""


# 表信息转换为对象
def initImports(fields):
    imports = []
    for field in fields:
        flag = field.javaType in JAVA_PACKAGE
        if flag:
            imports.append(JAVA_PACKAGE[field.javaType])
    return imports


def init_tables(generate_table):
    tables = []

    with DBUtils.DB(host='localhost', user='root', passwd='root', db='generate') as db:
        for gt in generate_table:
            tableObj = Table();
            tableObj.name = gt
            tableObj.className = StringUtils.firstUptoCameCase(gt).capitalize()

            table_sql = SQL_TABLE % gt
            db.execute(table_sql)
            table = db.fetchone()
            tableObj.comment = table[17]

            field_sql = SQL_TABLE_FIELD % gt
            db.execute(field_sql)
            fields = db.fetchall()

            tableObj.fields = initFields(fields)
            tableObj.imports = initImports(tableObj.fields)

            tables.append(tableObj)

    return tables


def initFields(fields):
    result = []

    for field in fields:
        fieldObj = Field()
        fieldObj.name = field[0]
        type = field[1]
        # 数据库类型携带的括号需要去掉
        le = type.find('(')
        fieldObj.type = type[:] if le == -1 else type[0:le]
        fieldObj.comment = field[8]
        fieldObj.javaType = JAVA_TYPE[fieldObj.type]
        fieldObj.javaName = StringUtils.toCameCase(fieldObj.name)
        fieldObj.culumn_constant = 'COLUMN_' + fieldObj.name.upper()
        fieldObj.field_constant = 'FIELD_' + fieldObj.name.upper()

        if fieldObj.PRI_KEY == field[4]:
            fieldObj.isPri = True

        fieldObj.valid = VALID[fieldObj.javaType] % fieldObj.comment
        result.append(fieldObj)
    return result


def createFile(type, outPath, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, fileName, table, otherImport, suffix='.java'):
    # 创建文件路劲
    out_path = outPath + PACKAGE[type].replace(".", "\\")
    createDir(out_path)

    t = Template(filename=TEMPLATE_PATH[type])

    var = t.render(class_name=table.className + FILE_SUFFIX[type], table=table, otherImport=otherImport,
                   package=PACKAGE)

    file_path = "%s\%s%s" % (out_path, fileName + FILE_SUFFIX[type], suffix)

    with open(file_path, mode='w', encoding='utf8') as file:
        file.write(var)


def createDir(path):
    flag = os.path.exists(path)
    if not flag:
        os.makedirs(path)


SQL_TABLE_FIELD = "SHOW FULL COLUMNS FROM %s"
SQL_TABLE = "show table status where Name = '%s'"

# 数据库映射字典
JAVA_TYPE = {
    'int': 'Integer',
    'bigint': 'Long',
    'decimal': 'BigDecimal',
    'varchar': 'String',
    'tinyint': 'boolean',
    'text': 'String',
    'mediumtext': 'String',
    'longtext': 'String',
    'timestamp': 'LocalDateTime',
    'datetime': 'LocalDateTime',
    'date': 'LocalDate',
}

# Java类型映射
JAVA_PACKAGE = {
    'BigDecimal': 'java.math.BigDecimal',
    'LocalDateTime': 'java.time.LocalDateTime',
    'LocalDate': 'java.time.LocalDate',
}

VALID = {
    'BigDecimal': '@NotNull(message="缺少%s")',
    'LocalDateTime': '@NotNull(message="缺少%s")',
    'LocalDate': '@NotNull(message="缺少%s")',
    'Integer': '@NotNull(message="缺少%s")',
    'Long': '@NotNull(message="缺少%s")',
    'String': '@NotBlank(message="缺少%s")',
    'boolean': '@NotNull(message="缺少%s")',
}

# 包定义
PACKAGE = {}
PACKAGE['BASE'] = "com.homedo.microservice.tools.wx.api"
PACKAGE['ENTITY'] = PACKAGE['BASE'] + ".bean.po"
PACKAGE['MAPPER'] = PACKAGE['BASE'] + ".persistence.mapper"
PACKAGE['DAO'] = PACKAGE['BASE'] + ".persistence.dao"
PACKAGE['DTO'] = PACKAGE['BASE'] + ".bean.dto"
PACKAGE['REQ'] = PACKAGE['BASE'] + ".bean.req"
PACKAGE['PAGEREQ'] = PACKAGE['BASE'] + ".bean.req"
PACKAGE['SERVICE'] = PACKAGE['BASE'] + ".service.basic"
PACKAGE['QUERY'] = PACKAGE['BASE'] + ".bean.query"
PACKAGE['RESP'] = PACKAGE['BASE'] + ".bean.resp"
PACKAGE['PAGERESP'] = PACKAGE['BASE'] + ".bean.resp"
PACKAGE['CONTROLLER'] = PACKAGE['BASE'] + ".controller"
PACKAGE['XML'] = "resources"

# 文件名后缀定义
FILE_SUFFIX = {}
FILE_SUFFIX['ENTITY'] = ""
FILE_SUFFIX['MAPPER'] = "Mapper"
FILE_SUFFIX['DAO'] = "Dao"
FILE_SUFFIX['SERVICE'] = "Service"
FILE_SUFFIX['CONTROLLER'] = "Controller"
FILE_SUFFIX['QUERY'] = "Query"
FILE_SUFFIX['DTO'] = "DTO"
FILE_SUFFIX['REQ'] = "Req"
FILE_SUFFIX['RESP'] = "Resp"
FILE_SUFFIX['LISTRESP'] = "ListResp"
FILE_SUFFIX['PAGERESP'] = "PageResp"
FILE_SUFFIX['CONTROLLER'] = "Controller"
FILE_SUFFIX['PAGEREQ'] = "PageReq"
FILE_SUFFIX['PAGERESP'] = "PageResp"
FILE_SUFFIX['XML'] = ""

# 模版位置
TEMPLATE_PATH = {
    'ENTITY': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Entity.text',
    'MAPPER': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Mapper.text',
    'XML': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Xml.text',
    'DAO': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Dao.text',
    'SERVICE': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Service.text',
    'DTO': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Dto.text',
    'REQ': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Req.text',
    'RESP': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Resp.text',
    'CONTROLLER': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\Controller.text',
    'PAGEREQ': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\PageReq.text',
    'PAGERESP': 'E:\\code\\cyanyunzi\\linwu-python\\generate\\template\\tk\\PageResp.text',
}

VALID_IMPORT = []
VALID_IMPORT.append("javax.validation.constraints.NotBlank")
VALID_IMPORT.append("org.springframework.format.annotation.DateTimeFormat")
VALID_IMPORT.append("javax.validation.constraints.NotNull")

if __name__ == '__main__':
    generate_table = ['test_field']

    OUT_FILE_PATH = "E:\\自动生成\\"

    MAPPER_XML_PACKAGE = ""

    tables = init_tables(generate_table)

    for table in tables:
        # 生成实体
        createFile("ENTITY", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table, [])

        # 生成mapper
        mapperOtherImport = []
        mapperOtherImport.append(PACKAGE['ENTITY'] + "." + table.className)
        createFile("MAPPER", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, "I" + table.className, table,
                   mapperOtherImport)

        # 生成XML
        createFile("XML", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.name, table,
                   [], ".xml")

        # 生成Dao
        daoOtherImport = []
        daoOtherImport.append(PACKAGE['ENTITY'] + "." + table.className)
        createFile("DAO", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table, daoOtherImport)

        # 生成Service
        serviceOtherImport = []
        serviceOtherImport.append(PACKAGE['ENTITY'] + "." + table.className)
        createFile("SERVICE", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table,
                   serviceOtherImport)

        # 生成DTO
        createFile("DTO", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table, [])

        # 生成Req
        reqOtherImport = []
        reqOtherImport.append(PACKAGE['BASE'] + "." + "bean.req.base.BaseReq")
        createFile("REQ", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table,
                   reqOtherImport + VALID_IMPORT)

        # 响应类
        respOtherImport = []
        respOtherImport.append(PACKAGE['BASE'] + "." + "bean.resp.base.BaseResp")
        respOtherImport.append("com.fasterxml.jackson.annotation.JsonFormat")
        createFile("RESP", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table, respOtherImport)

        # 控制器类
        conOtherImport = []
        respOtherImport.append(PACKAGE['BASE'] + "." + "bean.req." + table.className + "Req")
        respOtherImport.append(PACKAGE['BASE'] + "." + "bean.req." + table.className + "PageReq")
        respOtherImport.append(PACKAGE['BASE'] + "." + "bean.resp." + table.className + "Resp")
        respOtherImport.append(PACKAGE['BASE'] + "." + "bean.resp." + table.className + "PageResp")
        respOtherImport.append(PACKAGE['BASE'] + "." + "bean.base.resp.BasePageListResp")
        createFile("CONTROLLER", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table,
                   conOtherImport)

        # 生成分页Req
        page_req_other_import = []
        page_req_other_import.append(PACKAGE['BASE'] + "." + "bean.req.base.BasePageReq")
        createFile("PAGEREQ", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table,
                   page_req_other_import + VALID_IMPORT)

        # 生成分页响应类
        page_resp_other_import = []
        page_resp_other_import.append(PACKAGE['BASE'] + "." + "bean.resp.base.BasePageListResp")
        page_resp_other_import.append("com.fasterxml.jackson.annotation.JsonFormat")
        createFile("PAGERESP", OUT_FILE_PATH, PACKAGE, TEMPLATE_PATH, FILE_SUFFIX, table.className, table,
                   page_resp_other_import)

    os.system("explorer %s" % OUT_FILE_PATH)
