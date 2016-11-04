# -*- coding: utf-8 -*-
"""
Created on Wed Mar 16 15:40:29 2016

@author: okada

$Id: signature.py 177 2016-10-24 04:23:59Z aokada $
"""

########### js template
js_header = """(function() {
sig_data = {};
"""
js_dataset = """
sig_data.tooltip_format = {{
    signature_title:{signature_title},
    signature_partial:{signature_partial},
    mutation_title:{mutation_title},
    mutation_partial:{mutation_partial},
}};

sig_data.signatures = [{signatures}];
sig_data.sig_colors = [{colors}];
sig_data.dataset_sig = [{dataset_sig}];
sig_data.dataset_sig_max = {dataset_sig_max};
sig_data.route_id = [{route_id}];
sig_data.substitution = [{substruction}];
sig_data.Ids = [{Ids}];

// [ID, signature, value]
sig_data.mutations = [{mutations}];
"""

js_substruction_template = "{{name: '{name}', color: '{color}', route: [{route}],}},"

js_function = """
sig_data.esc_Ids = [];
for (var i=0; i < sig_data.Ids.length; i++) {
    sig_data.esc_Ids[i] = 'Key' + i;
}

function tooltip_text(format, obj) {
    var tooltip = [];
    for (var t in format.format) {
        tooltip.push(utils.text_format(format.format[t], obj));
    }
    return tooltip;
};

sig_data.get_data_par_signature = function (signature_id) {
    
    var tooltips = [];

    // par change
    for (var i=0; i < sig_data.substitution.length; i++) {
        
        var sum = 0;
        
        var obj = {
            'sig': sig_data.substitution[i].name,
        };
        tooltips[i] = [];
        segment_index = -1;
        for (var j=0; j < sig_data.dataset_sig[signature_id][i].length; j++) {
            if (j%16 == 0) {
                segment_index += 1;
                tooltips[i][segment_index] = [];
            }
            obj['route'] = sig_data.substitution[i].route[j];
            obj['#sum_item_value'] = sig_data.dataset_sig[signature_id][i][j];
            
            tooltips[i][segment_index].push(tooltip_text(sig_data.tooltip_format['signature_partial'], obj));
            sum += sig_data.dataset_sig[signature_id][i][j];
        }
        
        obj['#sum_group_value'] = sum;
        
        title = tooltip_text(sig_data.tooltip_format['signature_title'], obj);
        for (var s = 0; s < tooltips[i].length; s++) {
            for (var t = 0; t < title.length; t++) {
                tooltips[i][s].splice(t, 0, title[t]);
            }
        }
    }
    
    return {data: sig_data.dataset_sig[signature_id], tooltip: tooltips};
};

sig_data.get_bars_data = function () {
    
    var data = [];
    var keys = [];
    var tooltips = {};
    var sum_par_id = [];
    for (var i=0; i < sig_data.Ids.length; i++) {
        tooltips[sig_data.esc_Ids[i]] = [];
        sum_par_id[i] = 0;
    }
    
    // par func
    for (var f=0; f < sig_data.signatures.length; f++) {

        data[f] = [];
        keys[f] = [];

        // par ID
        for (var i=0; i < sig_data.Ids.length; i++) {
            
            var data_filt = sig_data.mutations.filter(function(item, index){
                if ((item[0] == i) && (item[1] == f)) return true;
            });
            
            //var sum = data_filt.length;
            var sum = 0;
            for (var s = 0; s < data_filt.length; s++) {
                sum += data_filt[s][2];
            }
            
            if (sum > 0) {
                data[f].push(sum);
                keys[f].push(sig_data.esc_Ids[i]);
                
                var obj = {
                    '#sum_mutaion_all': sig_data.mutations.length,
                    '#sum_item_value': sum,
                    'id': sig_data.Ids[i],
                    'sig': sig_data.signatures[f],
                };
                tooltips[sig_data.esc_Ids[i]].push(tooltip_text(sig_data.tooltip_format["mutation_partial"], obj));
                sum_par_id[i] += sum;
            }
        }
    }
    for (var i=0; i < sig_data.Ids.length; i++) {
        var obj = {
            '#sum_mutaion_all': sig_data.mutations.length,
            '#sum_item_value': sum_par_id[i],
            'id': sig_data.Ids[i],
        };
        
        title = tooltip_text(sig_data.tooltip_format["mutation_title"], obj);
        for (var t = 0; t < title.length; t++) {
            tooltips[sig_data.esc_Ids[i]].splice(t, 0, title[t]);
        }
    }
    
    return {data: data, key: keys, tooltip: tooltips};
};
})();
Object.freeze(sig_data);

"""

########### functions
def output_html(output_di, config):
    dataset = convert_tojs(output_di["data"], output_di["dir"] + "/" + output_di["js"], config)
    if dataset != None:
        create_html(dataset, output_di, config)
        return True
    
    return False
    
def convert_tojs(input_file, output_file, config):

    import json
    import math
    import itertools
    import paplot.subcode.tools as tools
    import paplot.convert as convert
    import paplot.color as color
    
    # data read
    try:
        jsonData = json.load(open(input_file[0]))
    except Exception as e:
        print ("failure open data %s, %s" % (input_file, e.message))
        return None
    
    key_Ids = tools.config_getstr(config, "result_format_signature", "key_id")
    key_signature = tools.config_getstr(config, "result_format_signature", "key_signature")
    key_mutations = tools.config_getstr(config, "result_format_signature", "key_mutation")
    
    sig_num = len(jsonData[key_signature])
    
    if sig_num == 0:
        print ("no data %s" % input_file)
        return None

    # signature names
    signature_list = []
    for s in range(sig_num):
        signature_list.append("signature %d" % (s+1))
        
    # each signature colors
    sig_color_list = color.create_color_array(sig_num, ["#f39700","#6cbb5a","#e60012","#00ada9","#e85298","#d7c447","#009944","#b6007a","#00a7db","#bb641d","#0079c2","#9b7cb6","#9CAEB7"])

    # axis-y max
    sig_y_max = tools.config_getint(config, "signature", "signature_y_max")
    if (sig_y_max < 0):
        for sig in jsonData[key_signature]:
            for sub in sig:
                m = max(sub)
                if sig_y_max < m:
                    sig_y_max = m
                    
    # route list
    sub_num = len(jsonData[key_signature][0][0])
    log = math.log(sub_num, 4)
    if log % 1 > 0:
        print ("substitution's list length is invalid (%d, not number 4^N)" % sub_num)
        return None

    route_id = []
    route_list = []
    for p in itertools.product(("A","C","G","T"), repeat = int(log)):
        route_id.append("".join(p))
        route_list.append(p)
        
    # substruction
    sub_di = [
        {"name":"C > A", "ref":"C", "color":tools.config_getstr(config, "signature", "alt_color_CtoA")},
        {"name":"C > G", "ref":"C", "color":tools.config_getstr(config, "signature", "alt_color_CtoG")},
        {"name":"C > T", "ref":"C", "color":tools.config_getstr(config, "signature", "alt_color_CtoT")},
        {"name":"T > A", "ref":"T", "color":tools.config_getstr(config, "signature", "alt_color_TtoA")},
        {"name":"T > C", "ref":"T", "color":tools.config_getstr(config, "signature", "alt_color_TtoC")},
        {"name":"T > G", "ref":"T", "color":tools.config_getstr(config, "signature", "alt_color_TtoG")},
    ]
    
    substruction = ""
    for sub in sub_di:
        route = []
        for r in route_list:
            route.append("p".join(r[0:int(log/2)]) + "p" + sub["ref"] + "p" + "p".join(r[int(log/2):]))
        
        substruction += js_substruction_template.format(name = sub["name"], color = sub["color"], route = convert.list_to_text(route))

    # mutations
    mutations_txt = ""
    for m in jsonData[key_mutations]:
        mutations_txt += "[%d,%d,%f]," % (m[0],m[1],m[2])
    
    # signature
    dataset_sig = ""
    for sig in jsonData[key_signature]:
        tmp = ""
        for sub in sig:
            tmp += "[" + ",".join(map(str, sub)) + "],"
        dataset_sig += ("[" + tmp + "],")
        
    # output
    keys_di = {"sig":"", "route":"", "id":""}
    f = open(output_file, "w")
    f.write(js_header \
        + js_dataset.format(Ids = convert.list_to_text(jsonData[key_Ids]), \
            signatures = convert.list_to_text(signature_list), \
            colors = convert.list_to_text(sig_color_list), \
            dataset_sig_max = sig_y_max, \
            mutations = mutations_txt, \
            dataset_sig = dataset_sig, \
            route_id = convert.list_to_text(route_id), \
            substruction = substruction, \
            signature_title = convert.pyformat_to_jstooltip_text(keys_di, config, "signature", "", "tooltip_format_signature_title"), \
            signature_partial = convert.pyformat_to_jstooltip_text(keys_di, config, "signature", "", "tooltip_format_signature_partial"), \
            mutation_title = convert.pyformat_to_jstooltip_text(keys_di, config, "signature", "", "tooltip_format_mutation_title"), \
            mutation_partial = convert.pyformat_to_jstooltip_text(keys_di, config, "signature", "", "tooltip_format_mutation_partial"), \
            )
        + js_function)
    f.close()

    return {"signature_num": sig_num} 

def create_html(dataset, output_di, config):
    import os
    import paplot.subcode.tools as tools
    import paplot.prep as prep
    
    html_div_template = "<div style='float: left;' id='div_pm{id}'></div>\n"
    html_add_template = "add_div('div_pm{id}');\n"

    div_text = ""
    add_text = ""
    for i in range(dataset["signature_num"]):
        
        div_text += html_div_template.format(id = i)
        add_text += html_add_template.format(id = i)

    f_template = open(os.path.dirname(os.path.abspath(__file__)) + "/templates/graph_signature.html")
    html_template = f_template.read()
    f_template.close()
    
    f_html = open(output_di["dir"] + "/" + output_di["html"], "w")
    f_html.write(
        html_template.format(project = output_di["project"], 
            title = "%s(#sig %d)" % (output_di["title"], output_di["sig_num"]),
            data_js = output_di["js"],
            version = prep.version_text(),
            date = tools.now_string(),
            divs = div_text,
            add_divs = add_text,
            style = "../style/%s" % os.path.basename(tools.config_getpath(config, "style", "path", "default.js")),
        ))
    f_html.close()
    
if __name__ == "__main__":
    pass