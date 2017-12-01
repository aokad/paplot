const assert = require('power-assert');

require('../src/js/utils.js');
require('../src/html/data_qc.js');
require('../src/html/data_mutation.js');
require('../src/html/data_ca.js');
require('../src/html/data_signature2.js');
require('../src/html/data_pmsignature2.js');

(function() {
    test_function = {};

    test_function.run = function() {
        describe('Tests data function...' , () => {
            describe('qc_data', () => {

                // TODO: , 区切りのtooltipテストケース追加

                it('qc_data.get_plot_config.1', () => {
                    var tooltip = qc_data.get_plot_config('chart_brush');
                    assert.equal(tooltip.title, '')
                })
                it('qc_data.get_plot_config.2', () => {
                    var tooltip = qc_data.get_plot_config('');
                    assert.equal(tooltip, null)
                })
                it('qc_data.get_dataset.1', () => {
                    var dataset = qc_data.get_dataset ('chart_brush');
                    assert.equal(dataset.data[0][0], 70.05);
                })
                it('qc_data.get_dataset.2', () => {
                    var dataset = qc_data.get_dataset ('chart_1');
                    assert.equal(dataset.data[0][0], 70.05);
                })
            })

            describe('ca_data', () => {

                // TODO: 不要関数削除
                // TODO: ca_data.get_arc_data_detail() から不要引数 'ID' 削除

                it('ca_data.get_data_thumb.1', () => {
                    var dataset = ca_data.get_data_thumb ('SAMPLE1');
                    assert.equal(dataset[0][11].start, '00_0011');
                    assert.deepEqual(dataset[0][11].ends, ['21_0002']);
                    assert.deepEqual(dataset[0][11].tooltip, []);
                })
                it('ca_data.get_data_thumb.2', () => {
                    var dataset = ca_data.get_data_thumb ('');
                    assert.equal(dataset[0][0].start, '00_0000');
                    assert.deepEqual(dataset[0][0].ends, []);
                    assert.deepEqual(dataset[0][0].tooltip, []);
                })
                it('ca_data.get_arc_data_thumb.1', () => {
                    var dataset = ca_data.get_arc_data_thumb ();
                    assert.equal(dataset[0].start, 'root.00.00_0000');
                    assert.deepEqual(dataset[0].ends, []);
                    assert.deepEqual(dataset[0].tooltip, []);
                })
                it('ca_data.get_data_detail.1', () => {
                    var dataset = ca_data.get_data_detail ('SAMPLE1');
                    assert.equal(dataset[0][23].start, '00_0023');
                    assert.deepEqual(dataset[0][23].ends, ['21_0005']);
                    assert.deepEqual(dataset[0][23].tooltip, [['[1] 153,160,367 (+) CEE2SPV1R1; [22] 33,751,554 (+) PVYYQIVS8G; inversion']]);
                })
                it('ca_data.get_data_detail.2', () => {
                    var dataset = ca_data.get_data_detail ('');
                    assert.equal(dataset[0][0].start, '00_0000');
                    assert.deepEqual(dataset[0][0].ends, []);
                    assert.deepEqual(dataset[0][0].tooltip, []);
                })
                it('ca_data.get_arc_data_detail.1', () => {
                    var dataset = ca_data.get_arc_data_detail ('SAMPLE1');
                    assert.equal(dataset[0].start, 'root.00.00_0000');
                    assert.deepEqual(dataset[0].ends, []);
                    assert.deepEqual(dataset[0].tooltip, []);
                })
                it('ca_data.get_select.1', () => {
                    var dataset = ca_data.get_select ();
                    assert.equal(dataset.value[0][0], 1);
                    assert.equal(dataset.key[0][0], 'root.17.17_0010');
                    assert.deepEqual(dataset.item[0][0], ['SAMPLE1']);
                })
            })
            describe('mut_data', () => {

            // TODO: 

                it('mut_data.get_dataset_id.1', () => {
                    var dataset = mut_data.get_dataset_id();
                    assert.equal(dataset.data[0][0], 2);
                    assert.equal(dataset.keys[0][0], 'SAMPLE00');
                    assert.deepEqual(dataset.tooltips["SAMPLE00"], [
                        'Sample:SAMPLE00, 21', 
                        ['Mutation Type:UTR3, 2'], 
                        ['Mutation Type:downstream, 1'], 
                        ['Mutation Type:exonic, 9'], 
                        ['Mutation Type:intergenic, 1'], 
                        ['Mutation Type:intronic, 8']
                    ]);
                })

                it('mut_data.get_dataset_checker.1', () => {
                    var dataset = mut_data.get_dataset_checker({'exonic': true}, ['KRAS']);
                    assert.deepEqual(dataset.data[0], [1, 1]);
                    assert.deepEqual(dataset.keys[0], ['SAMPLE00', 'SAMPLE33']);
                    assert.deepEqual(dataset.keys2[0], ['KRAS', 'KRAS']);
                    assert.deepEqual(dataset.tooltips[0], {'KRAS': ['Sample:SAMPLE00, Gene:KRAS, 2', 'Mutation Type[UTR3]', 'Mutation Type[exonic]']});
                })
                it('mut_data.get_dataset_gene.1', () => {
                    var dataset = mut_data.get_dataset_gene({'exonic': true}, 0, 10, ["number_of_mutations"], [false]);
                    assert.equal(dataset.data[3][0], 20);
                    assert.equal(dataset.keys[0][0], 'APC');
                    assert.deepEqual(dataset.tooltips['APC'], [
                        'Gene:APC, 25',
                        'Mutation Type:UTR3, 2',
                        'Mutation Type:UTR5, 2',
                        'Mutation Type:downstream, 4',
                        'Mutation Type:exonic, 12',
                        'Mutation Type:intronic, 4',
                        'Mutation Type:upstream, 1' ]
                    );
                })
                it('mut_data.get_id_nums.1', () => {
                    var dataset = mut_data.get_dataset_id();
                    var id_nums = mut_data.get_id_nums({'exonic': true}, dataset.data, dataset.keys);
                    assert.equal(id_nums[0], 21);
                })
                it('mut_data.get_id_flg_par_gene.1', () => {
                    var dataset = mut_data.get_id_flg_par_gene('SAMPLE00', {'exonic': true});
                    assert.equal(dataset[3], 1);
                })
                it('mut_data.get_sub_data.1', () => {
                    var dataset = mut_data.get_sub_data('sub0');
                    assert.deepEqual(dataset.stack[0].data[0], 1);
                    assert.deepEqual(dataset.stack[0].keys[0], 'SAMPLE03');
                    assert.equal(dataset.stack[0].color_n, '#0000ff');
                    assert.deepEqual(dataset.tooltips['SAMPLE00'], ['SAMPLE00, F']);
                    assert.deepEqual(dataset.label, {
                        type: 'fix',
                        text: [ 'Male', 'Female' ],
                        color: [ '#0000ff', '#ff0000' ] 
                    });
                })
                it('mut_data.get_sub_data.2', () => {
                    var dataset = mut_data.get_sub_data('sub1');
                    assert.deepEqual(dataset.stack[0].data[0], 1);
                    assert.deepEqual(dataset.stack[0].keys[0], 'SAMPLE21');
                    assert.equal(dataset.stack[0].color_n, '#E51721');
                    assert.deepEqual(dataset.tooltips['SAMPLE00'], ['SAMPLE00, 30']);
                    assert.deepEqual(dataset.label, {
                        type: 'range',
                        text: ['0-19', '20-39' ,'40-59' ,'60over'],
                        color: ['#E51721', '#0079BA', '#019A68', '#522886'] 
                    });
                })
                it('mut_data.get_sub_data.3', () => {
                    var dataset = mut_data.get_sub_data('sub2');
                    assert.deepEqual(dataset.stack[0].data[0], 1);
                    assert.deepEqual(dataset.stack[0].keys[0], 'SAMPLE26');
                    assert.equal(dataset.stack[0].color_n, '#0000ff');
                    assert.deepEqual(dataset.tooltips['SAMPLE00'], ['SAMPLE00, 40']);
                    assert.deepEqual(dataset.label, {
                        type: 'gradient',
                        text: ['Min(15)', 'Max(40)'],
                        color: ['#0000ff', '#ff0000'] 
                    });
                })

                it('mut_data.get_sub_values.1', () => {
                    var values = mut_data.get_sub_values('sub0');
                    assert.equal(values[0], 1)
                })
            })

            describe('sig_data', () => {

                it('var rect = sig_data.get_data_par_signature.1', () => {
                    var dataset = sig_data.get_data_par_signature(0);
                    assert.equal(dataset.data[0][0], 0.0021);
                    assert.equal(dataset.tooltip[0][0][0], 'C > A');
                    assert.deepEqual(dataset.tooltip[0][0][1], [ 'ApCpA:      0.00' ]);
                })
                it('var rect = sig_data.get_bars_data.1', () => {
                    var dataset = sig_data.get_bars_data(true);
                    assert.equal(dataset.data[0][0], 0.0882);
                    assert.equal(dataset.key[0][0], 'Key0');
                    assert.deepEqual(dataset.tooltip['Key0'],  [ 'PD3851a', [ 'Signature 1: 0.09' ], [ 'Signature 2: 0.91' ] ]);
                })
                it('var rect = sig_data.get_bars_data.2', () => {
                    var dataset = sig_data.get_bars_data(false);
                    assert.equal(dataset.data[0][0], 352.8882);
                    assert.equal(dataset.key[0][0], 'Key0');
                    assert.deepEqual(dataset.tooltip['Key0'], [ 'PD3851a', [ 'Signature 1: 352.89' ], [ 'Signature 2: 3647.71' ] ]);
                })
            })
            describe('msig_data', () => {

                it('var rect = msig_data.get_data_par_signature.1', () => {
                    var dataset = msig_data.get_dataset(0, 'alt');
                    assert.deepEqual(dataset.data[0], [ 0, 0, 0, 0 ]);
                    assert.equal(dataset.tooltip[0], "C -> A: 0.06");
                })
                it('var rect = msig_data.get_data_par_signature.2', () => {
                    var dataset = msig_data.get_dataset(0, 'ref0');
                    assert.equal(dataset.data[0], 0.189);
                    assert.equal(dataset.tooltip[0], "A: 0.19");
                })
                it('var rect = msig_data.get_data_par_signature.3', () => {
                    var dataset = msig_data.get_dataset(0, 'strand');
                    assert.equal(dataset.data[0], 0.514);
                    assert.equal(dataset.tooltip[0], "+ 0.51 - 0.48");
                })
                it('var rect = msig_data.get_bars_data.1', () => {
                    var dataset = msig_data.get_bars_data(true);
                    assert.equal(dataset.data[0][0], 0.09);
                    assert.equal(dataset.key[0][0], 'Key0');
                    assert.deepEqual(dataset.tooltip['Key0'],  [ 'PD3851a', [ 'Signature 1: 0.09' ], [ 'Background : 0.91' ] ]);
                })
                it('var rect = msig_data.get_bars_data.2', () => {
                    var dataset = msig_data.get_bars_data(false);
                    assert.equal(dataset.data[0][0], 71.64);
                    assert.equal(dataset.key[0][0], 'Key0');
                    assert.deepEqual(dataset.tooltip['Key0'], [ 'PD3851a', [ 'Signature 1: 71.64' ], [ 'Background : 723.56' ] ]);
                })
            })
        //  describe('utils', () => {
        //
        //    // TODO: 分割する
        //    
        //    it('var rect = utils.text_format.1', () => {
        //      var text = utils.text_format();
        //      console.log(text);
        //      assert.equal(text, "");
        //    })
        //    
        //  })
        })
    }
})();
