from unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5 import EVSCalibrationFit, DETECTOR_RANGE, \
     ENERGY_ESTIMATE, BRAGG_PEAK_CROP_RANGE, BRAGG_FIT_WINDOW_RANGE, RECOIL_PEAK_CROP_RANGE, RECOIL_FIT_WINDOW_RANGE, \
     RESONANCE_PEAK_CROP_RANGE, RESONANCE_FIT_WINDOW_RANGE
from mock import MagicMock, patch, call
from functools import partial

import unittest
import numpy as np


class TestVesuvioCalibrationFit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.set_cell_list = []

    @staticmethod
    def setup_mtd_mock(mock_obj, mock_dict):
        d = {}
        for key, return_obj in mock_dict.items():
            d[key] = return_obj
            mock_obj.__getitem__.side_effect = d.__getitem__

    def side_effect_set_cell(self, arg1, arg2, value):
        self.set_cell_list.append((arg1, arg2, value))

    @staticmethod
    def side_effect_cell(row_index, col_index, peaks):
        return peaks[row_index]

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CloneWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_filter_peaks_perfect_match(self, mock_mtd, mock_clone_workspace, mock_del_workspace):
        alg = EVSCalibrationFit()

        find_peaks_output_name = 'find_peaks_output_name'
        peak_estimates_list = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered = MagicMock()
        found_peaks = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered.column.return_value = found_peaks
        return_mock_find_peaks_output_name_unfiltered.cell.side_effect = partial(self.side_effect_cell, peaks=found_peaks)

        return_mock_find_peaks_output_name = MagicMock()
        return_mock_find_peaks_output_name.setRowCount = MagicMock()
        return_mock_find_peaks_output_name.columnCount.return_value = 1
        return_mock_find_peaks_output_name.rowCount.return_value = len(peak_estimates_list)
        return_mock_find_peaks_output_name.setCell.side_effect = self.side_effect_set_cell

        mtd_mock_dict = {'find_peaks_output_name': return_mock_find_peaks_output_name,
                         'find_peaks_output_name_unfiltered': return_mock_find_peaks_output_name_unfiltered}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        linear_bg_coeffs = (0, 0)
        alg._func_param_names = {"Position": 'LorentzPos'}
        alg._filter_found_peaks(find_peaks_output_name, peak_estimates_list, linear_bg_coeffs)
        self.assertEqual([(0, 0, found_peaks[0]), (1, 0, found_peaks[1]), (2, 0, found_peaks[2])],
                         self.set_cell_list)
        mock_clone_workspace.assert_called_with(InputWorkspace=return_mock_find_peaks_output_name,
                                                OutputWorkspace=find_peaks_output_name + '_unfiltered')
        mock_del_workspace.assert_called_with(find_peaks_output_name + '_unfiltered')


    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CloneWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_filter_peaks_no_match(self, mock_mtd, mock_clone_workspace, mock_del_workspace):
        alg = EVSCalibrationFit()

        find_peaks_output_name = 'find_peaks_output_name'
        peak_estimates_list = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered = MagicMock()
        found_peaks = []
        return_mock_find_peaks_output_name_unfiltered.column.return_value = found_peaks
        return_mock_find_peaks_output_name_unfiltered.cell.side_effect = partial(self.side_effect_cell, peaks=found_peaks)

        return_mock_find_peaks_output_name = MagicMock()
        return_mock_find_peaks_output_name.setRowCount = MagicMock()
        return_mock_find_peaks_output_name.columnCount.return_value = 1
        return_mock_find_peaks_output_name.rowCount.return_value = len(peak_estimates_list)
        return_mock_find_peaks_output_name.setCell.side_effect = self.side_effect_set_cell

        mtd_mock_dict = {'find_peaks_output_name': return_mock_find_peaks_output_name,
                         'find_peaks_output_name_unfiltered': return_mock_find_peaks_output_name_unfiltered}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        linear_bg_coeffs = (0, 0)
        alg._func_param_names = {"Position": 'LorentzPos'}
        alg._filter_found_peaks(find_peaks_output_name, peak_estimates_list, linear_bg_coeffs)
        self.assertEqual([], self.set_cell_list)
        mock_clone_workspace.assert_called_with(InputWorkspace=return_mock_find_peaks_output_name,
                                                OutputWorkspace=find_peaks_output_name + '_unfiltered')
        mock_del_workspace.assert_called_with(find_peaks_output_name + '_unfiltered')

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CloneWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_filter_peaks_one_match(self, mock_mtd, mock_clone_workspace, mock_del_workspace):
        alg = EVSCalibrationFit()

        find_peaks_output_name = 'find_peaks_output_name'
        peak_estimates_list = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered = MagicMock()
        found_peaks = [13000]
        return_mock_find_peaks_output_name_unfiltered.column.return_value = found_peaks
        return_mock_find_peaks_output_name_unfiltered.cell.side_effect = partial(self.side_effect_cell, peaks=found_peaks)

        return_mock_find_peaks_output_name = MagicMock()
        return_mock_find_peaks_output_name.setRowCount = MagicMock()
        return_mock_find_peaks_output_name.columnCount.return_value = 1
        return_mock_find_peaks_output_name.rowCount.return_value = len(peak_estimates_list)
        return_mock_find_peaks_output_name.setCell.side_effect = self.side_effect_set_cell

        mtd_mock_dict = {'find_peaks_output_name': return_mock_find_peaks_output_name,
                         'find_peaks_output_name_unfiltered': return_mock_find_peaks_output_name_unfiltered}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        linear_bg_coeffs = (0, 0)
        alg._func_param_names = {"Position": 'LorentzPos'}
        alg._filter_found_peaks(find_peaks_output_name, peak_estimates_list, linear_bg_coeffs)
        self.assertEqual([('LorentzPos', 0, peak_estimates_list[0]), (1, 0, found_peaks[0]), ('LorentzPos', 2, peak_estimates_list[2])],
                         self.set_cell_list)
        mock_clone_workspace.assert_called_with(InputWorkspace=return_mock_find_peaks_output_name,
                                                OutputWorkspace=find_peaks_output_name + '_unfiltered')
        mock_del_workspace.assert_called_with(find_peaks_output_name + '_unfiltered')

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CloneWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_filter_peaks_two_match(self, mock_mtd, mock_clone_workspace, mock_del_workspace):
        alg = EVSCalibrationFit()

        find_peaks_output_name = 'find_peaks_output_name'
        peak_estimates_list = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered = MagicMock()
        found_peaks = [9000, 16000]
        return_mock_find_peaks_output_name_unfiltered.column.return_value = found_peaks
        return_mock_find_peaks_output_name_unfiltered.cell.side_effect = partial(self.side_effect_cell, peaks=found_peaks)

        return_mock_find_peaks_output_name = MagicMock()
        return_mock_find_peaks_output_name.setRowCount = MagicMock()
        return_mock_find_peaks_output_name.columnCount.return_value = 1
        return_mock_find_peaks_output_name.rowCount.return_value = len(peak_estimates_list)
        return_mock_find_peaks_output_name.setCell.side_effect = self.side_effect_set_cell

        mtd_mock_dict = {'find_peaks_output_name': return_mock_find_peaks_output_name,
                         'find_peaks_output_name_unfiltered': return_mock_find_peaks_output_name_unfiltered}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        linear_bg_coeffs = (0, 0)
        alg._func_param_names = {"Position": 'LorentzPos'}
        alg._filter_found_peaks(find_peaks_output_name, peak_estimates_list, linear_bg_coeffs)
        self.assertEqual([(0, 0, found_peaks[0]), ('LorentzPos', 1, peak_estimates_list[1]), (2, 0, found_peaks[1])],
                         self.set_cell_list)
        mock_clone_workspace.assert_called_with(InputWorkspace=return_mock_find_peaks_output_name,
                                                OutputWorkspace=find_peaks_output_name + '_unfiltered')
        mock_del_workspace.assert_called_with(find_peaks_output_name + '_unfiltered')


    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CloneWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_filter_peaks_does_not_include_higher_found_peak(self, mock_mtd, mock_clone_workspace, mock_del_workspace):
        alg = EVSCalibrationFit()

        find_peaks_output_name = 'find_peaks_output_name'
        peak_estimates_list = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered = MagicMock()
        found_peaks = [9440, 15417, 16000]
        return_mock_find_peaks_output_name_unfiltered.column.return_value = found_peaks
        return_mock_find_peaks_output_name_unfiltered.cell.side_effect = partial(self.side_effect_cell, peaks=found_peaks)

        return_mock_find_peaks_output_name = MagicMock()
        return_mock_find_peaks_output_name.setRowCount = MagicMock()
        return_mock_find_peaks_output_name.columnCount.return_value = 1
        return_mock_find_peaks_output_name.rowCount.return_value = len(peak_estimates_list)
        return_mock_find_peaks_output_name.setCell.side_effect = self.side_effect_set_cell

        mtd_mock_dict = {'find_peaks_output_name': return_mock_find_peaks_output_name,
                         'find_peaks_output_name_unfiltered': return_mock_find_peaks_output_name_unfiltered}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        linear_bg_coeffs = (0, 0)
        alg._func_param_names = {"Position": 'LorentzPos'}
        alg._filter_found_peaks(find_peaks_output_name, peak_estimates_list, linear_bg_coeffs)
        self.assertEqual([(0, 0, found_peaks[0]), ('LorentzPos', 1, peak_estimates_list[1]), (2, 0, found_peaks[1])],
                         self.set_cell_list)
        mock_clone_workspace.assert_called_with(InputWorkspace=return_mock_find_peaks_output_name,
                                                OutputWorkspace=find_peaks_output_name + '_unfiltered')
        mock_del_workspace.assert_called_with(find_peaks_output_name + '_unfiltered')

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CloneWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_filter_peaks_does_not_include_lower_found_peak(self, mock_mtd, mock_clone_workspace, mock_del_workspace):
        alg = EVSCalibrationFit()

        find_peaks_output_name = 'find_peaks_output_name'
        peak_estimates_list = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered = MagicMock()
        found_peaks = [8000, 9440, 15417]
        return_mock_find_peaks_output_name_unfiltered.column.return_value = found_peaks
        return_mock_find_peaks_output_name_unfiltered.cell.side_effect = partial(self.side_effect_cell, peaks=found_peaks)

        return_mock_find_peaks_output_name = MagicMock()
        return_mock_find_peaks_output_name.setRowCount = MagicMock()
        return_mock_find_peaks_output_name.columnCount.return_value = 1
        return_mock_find_peaks_output_name.rowCount.return_value = len(peak_estimates_list)
        return_mock_find_peaks_output_name.setCell.side_effect = self.side_effect_set_cell

        mtd_mock_dict = {'find_peaks_output_name': return_mock_find_peaks_output_name,
                         'find_peaks_output_name_unfiltered': return_mock_find_peaks_output_name_unfiltered}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        linear_bg_coeffs = (0, 0)
        alg._func_param_names = {"Position": 'LorentzPos'}
        alg._filter_found_peaks(find_peaks_output_name, peak_estimates_list, linear_bg_coeffs)
        self.assertEqual([(0, 0, found_peaks[1]), ('LorentzPos', 1, peak_estimates_list[1]), (2, 0, found_peaks[2])],
                         self.set_cell_list)
        mock_clone_workspace.assert_called_with(InputWorkspace=return_mock_find_peaks_output_name,
                                                OutputWorkspace=find_peaks_output_name + '_unfiltered')
        mock_del_workspace.assert_called_with(find_peaks_output_name + '_unfiltered')


    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CloneWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_filter_peaks_handles_multiple_peaks(self, mock_mtd, mock_clone_workspace, mock_del_workspace):
        alg = EVSCalibrationFit()

        find_peaks_output_name = 'find_peaks_output_name'
        peak_estimates_list = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered = MagicMock()
        found_peaks = [8000, 9445, 13000, 13355, 15415, 16000]
        return_mock_find_peaks_output_name_unfiltered.column.return_value = found_peaks
        return_mock_find_peaks_output_name_unfiltered.cell.side_effect = partial(self.side_effect_cell, peaks=found_peaks)

        return_mock_find_peaks_output_name = MagicMock()
        return_mock_find_peaks_output_name.setRowCount = MagicMock()
        return_mock_find_peaks_output_name.columnCount.return_value = 1
        return_mock_find_peaks_output_name.rowCount.return_value = len(peak_estimates_list)
        return_mock_find_peaks_output_name.setCell.side_effect = self.side_effect_set_cell

        mtd_mock_dict = {'find_peaks_output_name': return_mock_find_peaks_output_name,
                         'find_peaks_output_name_unfiltered': return_mock_find_peaks_output_name_unfiltered}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        linear_bg_coeffs = (0, 0)
        alg._func_param_names = {"Position": 'LorentzPos'}
        alg._filter_found_peaks(find_peaks_output_name, peak_estimates_list, linear_bg_coeffs)
        self.assertEqual([(0, 0, found_peaks[1]), (1, 0, found_peaks[3]), (2, 0, found_peaks[4])], self.set_cell_list)
        mock_clone_workspace.assert_called_with(InputWorkspace=return_mock_find_peaks_output_name,
                                                OutputWorkspace=find_peaks_output_name + '_unfiltered')
        mock_del_workspace.assert_called_with(find_peaks_output_name + '_unfiltered')

    #Found peaks sometimes returns 'zero' peaks, usually at the end of the table workspace.
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CloneWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_filter_peaks_handles_zero_position_in_found_peaks(self, mock_mtd, mock_clone_workspace, mock_del_workspace):
        alg = EVSCalibrationFit()

        find_peaks_output_name = 'find_peaks_output_name'
        peak_estimates_list = [9440, 13351, 15417]
        return_mock_find_peaks_output_name_unfiltered = MagicMock()
        found_peaks = [9440, 13351, 0]
        return_mock_find_peaks_output_name_unfiltered.column.return_value = found_peaks
        return_mock_find_peaks_output_name_unfiltered.cell.side_effect = partial(self.side_effect_cell, peaks=found_peaks)

        return_mock_find_peaks_output_name = MagicMock()
        return_mock_find_peaks_output_name.setRowCount = MagicMock()
        return_mock_find_peaks_output_name.columnCount.return_value = 1
        return_mock_find_peaks_output_name.rowCount.return_value = len(peak_estimates_list)
        return_mock_find_peaks_output_name.setCell.side_effect = self.side_effect_set_cell

        mtd_mock_dict = {'find_peaks_output_name': return_mock_find_peaks_output_name,
                         'find_peaks_output_name_unfiltered': return_mock_find_peaks_output_name_unfiltered}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        linear_bg_coeffs = (0, 0)
        alg._func_param_names = {"Position": 'LorentzPos'}
        alg._filter_found_peaks(find_peaks_output_name, peak_estimates_list, linear_bg_coeffs)
        self.assertEqual([(0, 0, found_peaks[0]), (1, 0, found_peaks[1]), ('LorentzPos', 2, peak_estimates_list[2])], self.set_cell_list)
        mock_clone_workspace.assert_called_with(InputWorkspace=return_mock_find_peaks_output_name,
                                                OutputWorkspace=find_peaks_output_name + '_unfiltered')
        mock_del_workspace.assert_called_with(find_peaks_output_name + '_unfiltered')

    def test_estimate_bragg_peak_positions(self):
        def side_effect(arg1, arg2):
            if arg1 == 'L0':
                return 11.05
            elif arg1 == 'L1':
                return 0.5505
            elif arg1 == 't0':
                return -0.2
            elif arg1 == 'theta':
                return 139.5371

        alg = EVSCalibrationFit()
        alg._spec_list = [22]
        alg._read_param_column = MagicMock()
        alg._read_param_column.side_effect = side_effect
        alg._d_spacings = np.array([1.75, 2.475, 2.858])

        estimated_positions = alg._estimate_bragg_peak_positions()
        np.testing.assert_almost_equal([9629.84, 13619.43, 15727.03], estimated_positions.flatten().tolist(), 0.01)
        print(estimated_positions)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_check_nans_false(self, mock_mtd):
        alg = EVSCalibrationFit()
        table_ws = 'table_ws'
        data = [9440, np.nan, 15417]
        return_mock_obj_table_ws = MagicMock()
        return_mock_obj_table_ws.column.return_value = data
        return_mock_obj_table_ws.columnCount.return_value = len(data)

        mtd_mock_dict = {'table_ws': return_mock_obj_table_ws}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        self.assertFalse(alg._check_nans(table_ws))


    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_check_nans_true(self, mock_mtd):
        alg = EVSCalibrationFit()
        table_ws = 'table_ws'
        data = [9440, 13351, 15417]
        return_mock_obj_table_ws = MagicMock()
        return_mock_obj_table_ws.column.return_value = data
        return_mock_obj_table_ws.columnCount.return_value = len(data)

        mtd_mock_dict = {'table_ws': return_mock_obj_table_ws}

        self.setup_mtd_mock(mock_mtd, mtd_mock_dict)

        self.assertTrue(alg._check_nans(table_ws))


    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.ReplaceSpecialValues')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.EVSCalibrationFit._load_to_ads_and_crop')
    def test_preprocess_no_bg(self, mock_load_to_ads_and_crop, mock_replace_special_values):
        test_run_numbers = [1, 2, 3, 4]
        test_crop_range = [3, 10]
        test_sample_ws_name = "test_ws"

        alg = EVSCalibrationFit()
        alg._ws_crop_range = test_crop_range
        alg._sample_run_numbers = test_run_numbers
        alg._sample = test_sample_ws_name
        alg._bkg_run_numbers = []
        alg._preprocess()
        mock_load_to_ads_and_crop.assert_called_once_with(test_run_numbers, test_sample_ws_name, test_crop_range[0],
                                                          test_crop_range[-1])
        mock_replace_special_values.assert_called_once_with(test_sample_ws_name, NaNValue=0, NaNError=0, InfinityValue=0,
                                                            InfinityError=0, OutputWorkspace=test_sample_ws_name)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.EVSCalibrationFit._normalise_sample_by_background')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.ReplaceSpecialValues')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.EVSCalibrationFit._load_to_ads_and_crop')
    def test_preprocess_with_bg(self, mock_load_to_ads_and_crop, mock_replace_special_values, mock_normalise_sample):
        test_run_numbers = [1, 2, 3, 4]
        test_bg_run_numbers = [5, 6]
        test_crop_range = [3, 10]
        test_sample_ws_name = "test_ws"

        alg = EVSCalibrationFit()
        alg._ws_crop_range = test_crop_range
        alg._sample_run_numbers = test_run_numbers
        alg._sample = test_sample_ws_name
        alg._bkg_run_numbers = test_bg_run_numbers
        alg._background = test_bg_run_numbers[0]
        alg._preprocess()
        mock_load_to_ads_and_crop.assert_has_calls([call(test_run_numbers, test_sample_ws_name, test_crop_range[0],
                                                         test_crop_range[-1]),
                                                    call(test_bg_run_numbers, test_bg_run_numbers[0], test_crop_range[0],
                                                         test_crop_range[-1])])
        mock_normalise_sample.assert_called_once()
        mock_replace_special_values.assert_called_once_with(test_sample_ws_name, NaNValue=0, NaNError=0, InfinityValue=0,
                                                            InfinityError=0, OutputWorkspace=test_sample_ws_name)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CropWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.EVSCalibrationFit._load_files')
    def test_load_to_ads_and_crop(self, mock_load_files, mock_crop_workspace):
        alg = EVSCalibrationFit()
        run_numbers = [1, 2, 3, 4]
        output = "test_ws"
        xmin = 3
        xmax = 10

        alg._load_to_ads_and_crop(run_numbers, output, xmin, xmax)
        mock_load_files.assert_called_once_with(run_numbers, output)
        mock_crop_workspace.assert_called_once_with(output, XMin=xmin, XMax=xmax, OutputWorkspace=output)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.Divide')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.RebinToWorkspace')
    def test_normalise_sample_by_background(self, mock_rebin, mock_divide, mock_delete):
        alg = EVSCalibrationFit()
        sample_ws = 'test_ws'
        bg_ws = 'bg_ws'

        alg._sample = sample_ws
        alg._background = bg_ws

        alg._normalise_sample_by_background()
        mock_rebin.assert_called_once_with(WorkspaceToRebin=bg_ws, WorkspaceToMatch=sample_ws, OutputWorkspace=bg_ws)
        mock_divide.assert_called_once_with(sample_ws, bg_ws, OutputWorkspace=sample_ws)
        mock_delete.assert_called_once_with(bg_ws)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.Plus')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.EVSCalibrationFit._load_file')
    def test_load_files(self, mock_load_file, mock_plus, mock_delete):
        alg = EVSCalibrationFit()
        ws_numbers = ['1-4']  # Note this is parsed as '1-3', is this intentional?
        output_name = 'test_ws'
        alg._load_files(ws_numbers, output_name)
        mock_load_file.assert_has_calls([call('1', output_name), call('2', '__EVS_calib_temp_ws'),
                                         call('3', '__EVS_calib_temp_ws')])
        mock_plus.assert_has_calls([call(output_name, '__EVS_calib_temp_ws', OutputWorkspace=output_name),
                                    call(output_name, '__EVS_calib_temp_ws', OutputWorkspace=output_name)])
        mock_delete.assert_has_calls([call('__EVS_calib_temp_ws'), call('__EVS_calib_temp_ws')])

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.LoadRaw')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.LoadVesuvio')
    def test_load_file_vesuvio(self, mock_load_vesuvio, mock_load_raw):
        alg = EVSCalibrationFit()
        ws_name = 'test_file'
        output_name = 'test_ws'
        mode = 'FoilOut'
        spec_list = [3, 4, 5, 6]
        alg._mode = mode
        alg._spec_list = spec_list

        alg._load_file(ws_name, output_name)
        mock_load_vesuvio.assert_called_once_with(Filename=ws_name, Mode=mode, OutputWorkspace=output_name,
                                                  SpectrumList="%d-%d" % (spec_list[0], spec_list[-1]),
                                                  EnableLogging=False)
        mock_load_raw.assert_not_called()

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.ConvertToDistribution')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.LoadRaw')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.LoadVesuvio')
    def test_load_file_raw(self, mock_load_vesuvio, mock_load_raw, mock_convert_to_dist):
        alg = EVSCalibrationFit()
        ws_name = 'test_file'
        output_name = 'test_ws'
        mode = 'FoilOut'
        spec_list = [3, 4, 5, 6]
        alg._mode = mode
        alg._spec_list = spec_list
        mock_load_vesuvio.side_effect = RuntimeError()

        alg._load_file(ws_name, output_name)
        mock_load_raw.assert_called_once_with('EVS' + ws_name + '.raw', OutputWorkspace=output_name,
                                              SpectrumMin=spec_list[0], SpectrumMax=spec_list[-1],
                                              EnableLogging=False)
        mock_convert_to_dist.assert_called_once_with(output_name, EnableLogging=False)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.CreateEmptyTableWorkspace')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd', new_callable=dict)
    def test_create_output_parameters_table_ws(self, mock_mtd_module, mock_create_empty_table_ws):
        output_table_name = 'test_output_table'
        num_estimated_peaks = 3
        alg = EVSCalibrationFit()
        alg._generate_column_headers = MagicMock(return_value=['col1', 'col2', 'col3'])
        mock_output_table = MagicMock()
        mock_mtd_module[output_table_name] = mock_output_table

        alg._create_output_parameters_table_ws(output_table_name, num_estimated_peaks)
        mock_create_empty_table_ws.assert_called_once_with(OutputWorkspace=output_table_name)

        mock_output_table.addColumn.assert_any_call('int', 'Spectrum')
        for name in ['col1', 'col2', 'col3']:
            mock_output_table.addColumn.assert_any_call('double', name)
            alg._generate_column_headers.assert_called_once_with(num_estimated_peaks)

    def test_get_param_names(self):
        num_estimated_peaks = 3
        alg = EVSCalibrationFit()
        alg._func_param_names = {'key1': 'val1', 'key2': 'val2', 'key3': 'val3'}

        expected_param_names = ['f0.A0', 'f0.A1']
        for i in range(num_estimated_peaks):
            expected_param_names += ['f' + str(i) + '.' + name for name in alg._func_param_names.values()]

        param_names = alg._get_param_names(num_estimated_peaks)
        self.assertEqual(param_names, expected_param_names)

    def _setup_select_best_fit_params(self):
        alg = EVSCalibrationFit()
        spec_num = 1

        fit_results = {'params': [1, 2, 3], 'chi2': 10, 'status': 'success'}
        fit_results_u = {'params': [4, 5, 6], 'chi2': 8, 'status': 'success'}

        alg._prog_reporter = MagicMock()
        alg._prog_reporter.report = MagicMock()

        return alg, spec_num, fit_results, fit_results_u

    def test_select_best_fit_params_unconstrained_is_better(self):
        alg, spec_num, fit_results, fit_results_u = self._setup_select_best_fit_params()

        selected_params, unconstrained_fit_selected = alg._select_best_fit_params(spec_num, fit_results, fit_results_u)

        self.assertEqual(selected_params, fit_results_u['params'])
        self.assertTrue(unconstrained_fit_selected)

    def test_select_best_fit_params_constrained_is_better(self):
        alg, spec_num, fit_results, fit_results_u = self._setup_select_best_fit_params()
        fit_results['chi2'] = 6

        selected_params, unconstrained_fit_selected = alg._select_best_fit_params(spec_num, fit_results, fit_results_u)
        self.assertEqual(selected_params, fit_results['params'])
        self.assertFalse(unconstrained_fit_selected)

    def test_select_best_fit_params_unconstrained_has_invalid_peaks(self):
        alg, spec_num, fit_results, fit_results_u = self._setup_select_best_fit_params()
        fit_results_u['status'] = 'peaks invalid'

        selected_params, unconstrained_fit_selected = alg._select_best_fit_params(spec_num, fit_results,
                                                                                       fit_results_u)
        self.assertEqual(selected_params, fit_results['params'])
        self.assertFalse(unconstrained_fit_selected)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_output_params_to_table(self, mock_mtd_module):
        alg = EVSCalibrationFit()
        spec_num = 1
        num_estimated_peaks = 3
        output_table_name = 'test_output_table'

        alg._get_param_names = MagicMock(return_value=['A0', 'A1', 'param1', 'param2', 'param3'])

        param_values = [1, 2, 3, 4, 5]
        param_errors = [0.1, 0.2, 0.3, 0.4, 0.5]

        params = MagicMock()
        params.column.side_effect = lambda x: [['f0.A0', 'f0.A1', 'f1.param1', 'f1.param2', 'f1.param3'], param_values, param_errors][x]

        mock_output_table = MagicMock()
        mock_output_table.addRow = MagicMock()
        mock_mtd_module.__getitem__.return_value = mock_output_table

        alg._output_params_to_table(spec_num, num_estimated_peaks, params, output_table_name)

        alg._get_param_names.assert_called_once_with(num_estimated_peaks)
        params.column.assert_any_call(0)
        params.column.assert_any_call(1)
        params.column.assert_any_call(2)

        expected_row = [1, 0.1, 2, 0.2, 3, 0.3, 4, 0.4, 5, 0.5]
        mock_output_table.addRow.assert_called_once_with([spec_num] + expected_row)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    def test_get_output_and_clean_workspaces_unconstrained_not_performed(self, mock_delete_ws):
        alg = EVSCalibrationFit()
        find_peaks_output_name = 'test_find_output_name'
        fit_peaks_output_name = 'test_fit_output_name'
        output_ws = alg._get_output_and_clean_workspaces(False, False, find_peaks_output_name, fit_peaks_output_name)
        mock_delete_ws.assert_has_calls([call(fit_peaks_output_name + '_NormalisedCovarianceMatrix'),
                                         call(fit_peaks_output_name + '_Parameters'),
                                         call(find_peaks_output_name)])
        self.assertEqual(output_ws, fit_peaks_output_name + '_Workspace')

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    def test_get_output_and_clean_workspaces_unconstrained_performed(self, mock_delete_ws):
        alg = EVSCalibrationFit()
        find_peaks_output_name = 'test_find_output_name'
        fit_peaks_output_name = 'test_fit_output_name'
        output_ws = alg._get_output_and_clean_workspaces(True, False, find_peaks_output_name, fit_peaks_output_name)
        mock_delete_ws.assert_has_calls([call(fit_peaks_output_name + '_NormalisedCovarianceMatrix'),
                                         call(fit_peaks_output_name + '_Parameters'),
                                         call(find_peaks_output_name),
                                         call(fit_peaks_output_name + '_unconstrained' + '_NormalisedCovarianceMatrix'),
                                         call(fit_peaks_output_name + '_unconstrained' + '_Parameters'),
                                         call(find_peaks_output_name + '_unconstrained'),
                                         call(fit_peaks_output_name + '_unconstrained' + '_Workspace')])
        self.assertEqual(output_ws, fit_peaks_output_name + '_Workspace')

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.DeleteWorkspace')
    def test_get_output_and_clean_workspaces_unconstrained_performed_and_selected(self, mock_delete_ws):
        alg = EVSCalibrationFit()
        find_peaks_output_name = 'test_find_output_name'
        fit_peaks_output_name = 'test_fit_output_name'
        output_ws = alg._get_output_and_clean_workspaces(True, True, find_peaks_output_name, fit_peaks_output_name)
        mock_delete_ws.assert_has_calls([call(fit_peaks_output_name + '_NormalisedCovarianceMatrix'),
                                         call(fit_peaks_output_name + '_Parameters'),
                                         call(find_peaks_output_name),
                                         call(fit_peaks_output_name + '_unconstrained' + '_NormalisedCovarianceMatrix'),
                                         call(fit_peaks_output_name + '_unconstrained' + '_Parameters'),
                                         call(find_peaks_output_name + '_unconstrained'),
                                         call(fit_peaks_output_name + '_Workspace')])
        self.assertEqual(output_ws, fit_peaks_output_name + '_unconstrained' + '_Workspace')

    def test_generate_column_headers(self):
        alg = EVSCalibrationFit()
        num_estimated_peaks = 3

        alg._get_param_names = MagicMock(return_value=['A0', 'A1', 'val1', 'val2', 'val3'])

        col_headers = alg._generate_column_headers(num_estimated_peaks)

        alg._get_param_names.assert_called_once_with(num_estimated_peaks)

        expected_col_headers = ['A0', 'A0_Err', 'A1', 'A1_Err', 'val1', 'val1_Err', 'val2', 'val2_Err', 'val3', 'val3_Err']
        self.assertEqual(col_headers, expected_col_headers)

    def test_get_unconstrained_ws_name(self):
        alg = EVSCalibrationFit()
        ws_name = 'test'
        return_ws_name = alg._get_unconstrained_ws_name(ws_name)
        self.assertEqual(ws_name + '_unconstrained', return_ws_name)

    def _setup_run_find_peaks_test(self, unconstrained):
        alg = EVSCalibrationFit()
        alg._sample = 'sample_workspace'
        workspace_index = 0
        find_peaks_output_name = 'peaks_list'
        find_peaks_input_params = {'Param1': 1, 'Param2': 3}
        fn_args = {'workspace_index': workspace_index, 'find_peaks_output_name': find_peaks_output_name,
                   'find_peaks_input_params': find_peaks_input_params, 'unconstrained': unconstrained}
        return alg, fn_args

    @staticmethod
    def _setup_mtd_mock(mtd_mock_obj, find_peaks_name, peaks_found):
        mock_find_peaks_output = MagicMock()
        mock_find_peaks_output.rowCount.return_value = peaks_found
        mtd_mock_obj.__getitem__.side_effect = lambda name: mock_find_peaks_output if\
            name == find_peaks_name else None

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.FindPeaks')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_run_find_peaks_peaks_found(self, mock_mtd_module, mock_find_peaks):
        alg, fn_args = self._setup_run_find_peaks_test(unconstrained=False)

        self._setup_mtd_mock(mock_mtd_module, fn_args['find_peaks_output_name'], 1)

        result = alg._run_find_peaks(**fn_args)
        mock_find_peaks.assert_called_once()
        self.assertTrue(result)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.FindPeaks')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_run_find_peaks_no_peaks_found_raises_value_error(self, mock_mtd_module, mock_find_peaks):
        alg, fn_args = self._setup_run_find_peaks_test(unconstrained=False)

        self._setup_mtd_mock(mock_mtd_module, fn_args['find_peaks_output_name'], 0)

        with self.assertRaises(ValueError, msg="Error finding peaks."):
            alg._run_find_peaks(**fn_args)
        mock_find_peaks.assert_called_once()

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.FindPeaks')
    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.mtd')
    def test_run_find_peaks_unconstrained_no_peaks_found_no_error(self, mock_mtd_module, mock_find_peaks):
        alg, fn_args = self._setup_run_find_peaks_test(unconstrained=True)

        self._setup_mtd_mock(mock_mtd_module, fn_args['find_peaks_output_name'], 0)

        result = alg._run_find_peaks(**fn_args)
        mock_find_peaks.assert_called_once()
        self.assertFalse(result)

    @patch('unpackaged.vesuvio_calibration.calibrate_vesuvio_uranium_martyn_MK5.FindPeaks')
    def test_run_find_peaks_unconstrained_peaks_found_raises_error(self, mock_find_peaks):
        alg, fn_args = self._setup_run_find_peaks_test(unconstrained=True)

        mock_find_peaks.side_effect = ValueError

        result = alg._run_find_peaks(**fn_args)
        mock_find_peaks.assert_called_once()
        self.assertFalse(result)

if __name__ == '__main__':
    unittest.main()
