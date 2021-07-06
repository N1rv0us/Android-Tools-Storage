'''
    查询apk或是dex文件中，所有包含某种Annoations的方法，样例：查询所有@JavascriptInterface
'''

from androguard.misc import AnalyzeAPK

def filter_annoations_method(d,filter):
    ret = []

    for dvm in d:
        for adi in dvm.map_list.get_item_type("TYPE_ANNOTATIONS_DIRECTORY_ITEM"):
            for mi in adi.get_method_annotations():
                #print(repr(dvm.get_method_by_idx(mi.get_method_idx())))

                ann_set_item = dvm.CM.get_obj_by_offset(mi.get_annotations_off())
                for aoffitem in ann_set_item.get_annotation_off_item():
                    annotation_item = dvm.CM.get_obj_by_offset(aoffitem.get_annotation_off())
                    encode_annotation = annotation_item.get_annotation()
                    #print("@{}".format(dvm.CM.get_type(encode_annotation.get_type_idx())))
                    annotation_str = dvm.CM.get_type(encode_annotation.get_type_idx())
                    # annotation filter here
                    # print("@{}".format(annotation_str))
                    if filter not in annotation_str:
                        break
                    tmp = {}
                    js_method = dvm.get_method_by_idx(mi.get_method_idx())
                    
                    tmp["class"] = js_method.get_class_name()
                    tmp["method"] = js_method.get_name()
                    tmp["descriptor"] = js_method.get_descriptor()

                    ret.append(tmp)

    return ret
if __name__ == "__main__":
    a,d,dx = AnalyzeAPK("path2apk-file")
    annotation_methods = filter_annoations_method(d,"Landroid/webkit/JavascriptInterface;")
    print("======= result =======")
    print(annotation_methods)