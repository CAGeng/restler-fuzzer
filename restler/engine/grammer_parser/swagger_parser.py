import json
import logging


class swagger_parser(object):
    def __init__(self, filepath):
        with open(filepath, 'r') as f:
            self.swagger = json.load(f)

        self.logger = logging.getLogger('swagger_parser')
        self.logger.setLevel(logging.DEBUG)
        handler = logging.FileHandler("./swagger_parser.log")
        handler.setLevel(logging.DEBUG)
        self.logger.addHandler(handler)

    def parse(self):
        self.enhance_parameter()
        return self

    def enhance_parameter(self):
        for endpoint in self.swagger['paths'].keys():
            for method in self.swagger['paths'][endpoint].keys():
                if 'parameters' in self.swagger['paths'][endpoint][method]:
                    for param in self.swagger['paths'][endpoint][method]['parameters']:
                        if 'schema' in param:
                            schema = param['schema']
                            if 'historical' in schema and schema['historical']:
                                request = self.get_request(endpoint, method)
                                self.logger.debug(str(request))

                                # 定位该param位置
                                if param['in'] == 'path':
                                    index = endpoint.find('{' + param['name'] + '}')
                                    if index != -1:
                                        position = endpoint[:index].count('/')
                                        param_record = Param(Param.Param_type.PATH).set_path_position(position)

                                        # 修改definition条目保存记录
                                        definition_entry, ind = self.get_definition_entry(request, param_record)
                                        request.definition[ind] = definition_entry + ('historical',)

    # 对原始的req_collection，在位的更改
    def set_basic_req_collection(self, basic_req_collection):
        self.req_collection = basic_req_collection
        return self

    # 定位request的definition条目所在，用来增强request
    # 并返回definition在列表的位置，用来在位的修改
    def get_definition_entry(self, request, param):
        if param.type == param.Param_type.PATH:
            path_position = param.position
            pos_con = 0
            ind = 0
            for definition in request.definition:
                if pos_con == path_position:
                    return definition, ind
                if definition[1] == '/':
                    pos_con += 1
                ind += 1

    # 定位request在request_collection中的位置
    def get_request(self, endpoint, method):
        for request_id in self.req_collection.request_id_collection.keys():
            endpoint_requests = self.req_collection.request_id_collection[request_id]
            for request in endpoint_requests:
                # 注意不要用request.endpoint，它是填写了动态字段的，e.g. /api/fuzzstring
                if request.endpoint_no_dynamic_objects == endpoint and request.method.lower() == method.lower():
                    return request

class Param(object):

    import enum
    class Param_type(enum.Enum):
        PATH = 1
        BODY = 2

    def __init__(self, type : Param_type):
        self.type = type

    def set_path_position(self, position : int):
        if self.type == self.Param_type.PATH:
            self.position = position
        else:
            raise Exception("Param type is not PATH")
        return self

    def set_body_position(self, position : int):
        if self.type == self.Param_type.BODY:
            self.position = position
        else:
            raise Exception("Param type is not BODY")
        return self

