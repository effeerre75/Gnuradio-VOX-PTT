#!/usr/bin/env python2
##################################################
# GNU Radio Python Flow Graph
# Title: Red Pitaya Digi Trx Usb
# Generated: Wed Dec 23 16:00:49 2015
##################################################

if __name__ == '__main__':
    import ctypes
    import sys
    if sys.platform.startswith('linux'):
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"

from PyQt4 import Qt
from gnuradio import analog
from gnuradio import audio
from gnuradio import blocks
from gnuradio import eng_notation
from gnuradio import filter
from gnuradio import gr
from gnuradio import qtgui
from gnuradio.eng_option import eng_option
from gnuradio.filter import firdes
from gnuradio.qtgui import Range, RangeWidget
from grc_gnuradio import blks2 as grc_blks2
from optparse import OptionParser
import red_pitaya
import sip
import sys
import threading
import time


class Red_Pitaya_digi_trx_USB(gr.top_block, Qt.QWidget):

    def __init__(self):
        gr.top_block.__init__(self, "Red Pitaya Digi Trx Usb")
        Qt.QWidget.__init__(self)
        self.setWindowTitle("Red Pitaya Digi Trx Usb")
        try:
             self.setWindowIcon(Qt.QIcon.fromTheme('gnuradio-grc'))
        except:
             pass
        self.top_scroll_layout = Qt.QVBoxLayout()
        self.setLayout(self.top_scroll_layout)
        self.top_scroll = Qt.QScrollArea()
        self.top_scroll.setFrameStyle(Qt.QFrame.NoFrame)
        self.top_scroll_layout.addWidget(self.top_scroll)
        self.top_scroll.setWidgetResizable(True)
        self.top_widget = Qt.QWidget()
        self.top_scroll.setWidget(self.top_widget)
        self.top_layout = Qt.QVBoxLayout(self.top_widget)
        self.top_grid_layout = Qt.QGridLayout()
        self.top_layout.addLayout(self.top_grid_layout)

        self.settings = Qt.QSettings("GNU Radio", "Red_Pitaya_digi_trx_USB")
        self.restoreGeometry(self.settings.value("geometry").toByteArray())

        ##################################################
        # Variables
        ##################################################
        self.shift = shift = 1700
        self.samp_rate = samp_rate = 48000
        self.rx_samp_rate = rx_samp_rate = 20000
        self.rx_freq = rx_freq = 14095600
        self.rx_amp = rx_amp = 200
        self.ptt = ptt = 0
        self.monitor = monitor = 1
        self.mon_vol = mon_vol = 200
        self.fL = fL = 300
        self.fH = fH = 3000
        self.addr = addr = "192.168.123.73"

        ##################################################
        # Blocks
        ##################################################
        self.probe = blocks.probe_signal_f()
        self._shift_range = Range(0, 3000, 1, 1700, 200)
        self._shift_win = RangeWidget(self._shift_range, self.set_shift, "TX Shift", "counter", float)
        self.top_grid_layout.addWidget(self._shift_win, 1,7,1,1)
        self._rx_freq_range = Range(10, 60000000, 100, 14095600, 200)
        self._rx_freq_win = RangeWidget(self._rx_freq_range, self.set_rx_freq, "Freq.", "counter", float)
        self.top_grid_layout.addWidget(self._rx_freq_win, 1,1,1,1)
        self._rx_amp_range = Range(10, 10000, 10, 200, 200)
        self._rx_amp_win = RangeWidget(self._rx_amp_range, self.set_rx_amp, "RX Amp", "counter", float)
        self.top_grid_layout.addWidget(self._rx_amp_win, 1,6,1,1)
        def _ptt_probe():
            while True:
                val = self.probe.level()
                try:
                    self.set_ptt(val)
                except AttributeError:
                    pass
                time.sleep(1.0 / (10))
        _ptt_thread = threading.Thread(target=_ptt_probe)
        _ptt_thread.daemon = True
        _ptt_thread.start()
        _monitor_check_box = Qt.QCheckBox("monitor")
        self._monitor_choices = {True: 0, False: 1}
        self._monitor_choices_inv = dict((v,k) for k,v in self._monitor_choices.iteritems())
        self._monitor_callback = lambda i: Qt.QMetaObject.invokeMethod(_monitor_check_box, "setChecked", Qt.Q_ARG("bool", self._monitor_choices_inv[i]))
        self._monitor_callback(self.monitor)
        _monitor_check_box.stateChanged.connect(lambda i: self.set_monitor(self._monitor_choices[bool(i)]))
        self.top_grid_layout.addWidget(_monitor_check_box, 1,4,1,1)
        self._mon_vol_range = Range(10, 8000, 10, 200, 200)
        self._mon_vol_win = RangeWidget(self._mon_vol_range, self.set_mon_vol, "Volume", "counter", float)
        self.top_grid_layout.addWidget(self._mon_vol_win, 1,5,1,1)
        self._fL_range = Range(0, 5000, 10, 300, 200)
        self._fL_win = RangeWidget(self._fL_range, self.set_fL, "Filter Cut Low", "counter", float)
        self.top_grid_layout.addWidget(self._fL_win, 1,2,1,1)
        self._fH_range = Range(0, 5000, 10, 3000, 200)
        self._fH_win = RangeWidget(self._fH_range, self.set_fH, "Filter Cut High", "counter", float)
        self.top_grid_layout.addWidget(self._fH_win, 1,3,1,1)
        self.red_pitaya_source_0 = red_pitaya.source(
                addr=str(addr),
                port=1001,
                freq=rx_freq,
                rate=rx_samp_rate,
                corr=0
        )
          
        self.red_pitaya_sink_0 = red_pitaya.sink(
                addr=str(addr),
                port=1001,
                freq=rx_freq+shift,
                rate=rx_samp_rate,
                corr=0,
                ptt=ptt
        )
          
        self.rational_resampler_xxx_1 = filter.rational_resampler_fff(
                interpolation=rx_samp_rate/2000,
                decimation=24,
                taps=None,
                fractional_bw=None,
        )
        self.rational_resampler_xxx_0 = filter.rational_resampler_ccc(
                interpolation=24,
                decimation=rx_samp_rate/2000,
                taps=None,
                fractional_bw=None,
        )
        self.qtgui_time_sink_x_0_0 = qtgui.time_sink_c(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0_0.set_y_axis(-0.5, 0.5)
        
        self.qtgui_time_sink_x_0_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0_0.enable_tags(-1, False)
        self.qtgui_time_sink_x_0_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0, 0, 0, "")
        self.qtgui_time_sink_x_0_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0_0.enable_grid(True)
        self.qtgui_time_sink_x_0_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_time_sink_x_0_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["dark red", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(2*1):
            if len(labels[i]) == 0:
                if(i % 2 == 0):
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Re{{Data {0}}}".format(i/2))
                else:
                    self.qtgui_time_sink_x_0_0.set_line_label(i, "Im{{Data {0}}}".format(i/2))
            else:
                self.qtgui_time_sink_x_0_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_0_win)
        self.qtgui_time_sink_x_0 = qtgui.time_sink_f(
        	1024, #size
        	samp_rate, #samp_rate
        	"", #name
        	1 #number of inputs
        )
        self.qtgui_time_sink_x_0.set_update_time(0.10)
        self.qtgui_time_sink_x_0.set_y_axis(-0.5, 0.5)
        
        self.qtgui_time_sink_x_0.set_y_label("Amplitude", "")
        
        self.qtgui_time_sink_x_0.enable_tags(-1, False)
        self.qtgui_time_sink_x_0.set_trigger_mode(qtgui.TRIG_MODE_FREE, qtgui.TRIG_SLOPE_POS, 0, 0, 0, "")
        self.qtgui_time_sink_x_0.enable_autoscale(False)
        self.qtgui_time_sink_x_0.enable_grid(True)
        self.qtgui_time_sink_x_0.enable_control_panel(False)
        
        if not False:
          self.qtgui_time_sink_x_0.disable_legend()
        
        labels = ["", "", "", "", "",
                  "", "", "", "", ""]
        widths = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        colors = ["blue", "red", "green", "black", "cyan",
                  "magenta", "yellow", "dark red", "dark green", "blue"]
        styles = [1, 1, 1, 1, 1,
                  1, 1, 1, 1, 1]
        markers = [-1, -1, -1, -1, -1,
                   -1, -1, -1, -1, -1]
        alphas = [1.0, 1.0, 1.0, 1.0, 1.0,
                  1.0, 1.0, 1.0, 1.0, 1.0]
        
        for i in xrange(1):
            if len(labels[i]) == 0:
                self.qtgui_time_sink_x_0.set_line_label(i, "Data {0}".format(i))
            else:
                self.qtgui_time_sink_x_0.set_line_label(i, labels[i])
            self.qtgui_time_sink_x_0.set_line_width(i, widths[i])
            self.qtgui_time_sink_x_0.set_line_color(i, colors[i])
            self.qtgui_time_sink_x_0.set_line_style(i, styles[i])
            self.qtgui_time_sink_x_0.set_line_marker(i, markers[i])
            self.qtgui_time_sink_x_0.set_line_alpha(i, alphas[i])
        
        self._qtgui_time_sink_x_0_win = sip.wrapinstance(self.qtgui_time_sink_x_0.pyqwidget(), Qt.QWidget)
        self.top_layout.addWidget(self._qtgui_time_sink_x_0_win)
        self.fft_filter_xxx_0_0 = filter.fft_filter_ccc(1, (firdes.complex_band_pass(1, rx_samp_rate, fL, fH, 100, firdes.WIN_HAMMING )), 1)
        self.fft_filter_xxx_0_0.declare_sample_delay(0)
        self.fft_filter_xxx_0 = filter.fft_filter_ccc(1, (firdes.complex_band_pass(1, rx_samp_rate, fL, fH, 100, firdes.WIN_HAMMING )), 1)
        self.fft_filter_xxx_0.declare_sample_delay(0)
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vff((mon_vol, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vff((rx_amp, ))
        self.blocks_float_to_complex_0 = blocks.float_to_complex(1)
        self.blocks_complex_to_real_0 = blocks.complex_to_real(1)
        self.blks2_valve_0_0 = grc_blks2.valve(item_size=gr.sizeof_float*1, open=bool(monitor))
        self.blks2_valve_0 = grc_blks2.valve(item_size=gr.sizeof_gr_complex*1, open=bool(ptt))
        self.audio_source_0 = audio.source(samp_rate, "Soundflower (2ch)", True)
        self.audio_sink_1_0 = audio.sink(samp_rate, "Built-In Output", True)
        self.audio_sink_1 = audio.sink(samp_rate, "Soundflower (64ch)", True)
        self.analog_const_source_x_0 = analog.sig_source_f(0, analog.GR_CONST_WAVE, 0, 0, 0)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.analog_const_source_x_0, 0), (self.blocks_float_to_complex_0, 1))    
        self.connect((self.audio_source_0, 0), (self.probe, 0))    
        self.connect((self.audio_source_0, 0), (self.rational_resampler_xxx_1, 0))    
        self.connect((self.blks2_valve_0, 0), (self.fft_filter_xxx_0, 0))    
        self.connect((self.blks2_valve_0_0, 0), (self.blocks_multiply_const_vxx_0_0, 0))    
        self.connect((self.blocks_complex_to_real_0, 0), (self.blocks_multiply_const_vxx_0, 0))    
        self.connect((self.blocks_float_to_complex_0, 0), (self.fft_filter_xxx_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.audio_sink_1, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blks2_valve_0_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.qtgui_time_sink_x_0, 0))    
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.audio_sink_1_0, 0))    
        self.connect((self.fft_filter_xxx_0, 0), (self.rational_resampler_xxx_0, 0))    
        self.connect((self.fft_filter_xxx_0_0, 0), (self.qtgui_time_sink_x_0_0, 0))    
        self.connect((self.fft_filter_xxx_0_0, 0), (self.red_pitaya_sink_0, 0))    
        self.connect((self.rational_resampler_xxx_0, 0), (self.blocks_complex_to_real_0, 0))    
        self.connect((self.rational_resampler_xxx_1, 0), (self.blocks_float_to_complex_0, 0))    
        self.connect((self.red_pitaya_source_0, 0), (self.blks2_valve_0, 0))    

    def closeEvent(self, event):
        self.settings = Qt.QSettings("GNU Radio", "Red_Pitaya_digi_trx_USB")
        self.settings.setValue("geometry", self.saveGeometry())
        event.accept()

    def get_shift(self):
        return self.shift

    def set_shift(self, shift):
        self.shift = shift
        self.red_pitaya_sink_0.set_freq(self.rx_freq+self.shift, 0)

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.qtgui_time_sink_x_0.set_samp_rate(self.samp_rate)
        self.qtgui_time_sink_x_0_0.set_samp_rate(self.samp_rate)

    def get_rx_samp_rate(self):
        return self.rx_samp_rate

    def set_rx_samp_rate(self, rx_samp_rate):
        self.rx_samp_rate = rx_samp_rate
        self.fft_filter_xxx_0.set_taps((firdes.complex_band_pass(1, self.rx_samp_rate, self.fL, self.fH, 100, firdes.WIN_HAMMING )))
        self.fft_filter_xxx_0_0.set_taps((firdes.complex_band_pass(1, self.rx_samp_rate, self.fL, self.fH, 100, firdes.WIN_HAMMING )))
        self.red_pitaya_sink_0.set_rate(self.rx_samp_rate)
        self.red_pitaya_source_0.set_rate(self.rx_samp_rate)

    def get_rx_freq(self):
        return self.rx_freq

    def set_rx_freq(self, rx_freq):
        self.rx_freq = rx_freq
        self.red_pitaya_sink_0.set_freq(self.rx_freq+self.shift, 0)
        self.red_pitaya_source_0.set_freq(self.rx_freq, 0)

    def get_rx_amp(self):
        return self.rx_amp

    def set_rx_amp(self, rx_amp):
        self.rx_amp = rx_amp
        self.blocks_multiply_const_vxx_0.set_k((self.rx_amp, ))

    def get_ptt(self):
        return self.ptt

    def set_ptt(self, ptt):
        self.ptt = ptt
        self.blks2_valve_0.set_open(bool(self.ptt))
        self.red_pitaya_sink_0.set_ptt(self.ptt)

    def get_monitor(self):
        return self.monitor

    def set_monitor(self, monitor):
        self.monitor = monitor
        self._monitor_callback(self.monitor)
        self.blks2_valve_0_0.set_open(bool(self.monitor))

    def get_mon_vol(self):
        return self.mon_vol

    def set_mon_vol(self, mon_vol):
        self.mon_vol = mon_vol
        self.blocks_multiply_const_vxx_0_0.set_k((self.mon_vol, ))

    def get_fL(self):
        return self.fL

    def set_fL(self, fL):
        self.fL = fL
        self.fft_filter_xxx_0.set_taps((firdes.complex_band_pass(1, self.rx_samp_rate, self.fL, self.fH, 100, firdes.WIN_HAMMING )))
        self.fft_filter_xxx_0_0.set_taps((firdes.complex_band_pass(1, self.rx_samp_rate, self.fL, self.fH, 100, firdes.WIN_HAMMING )))

    def get_fH(self):
        return self.fH

    def set_fH(self, fH):
        self.fH = fH
        self.fft_filter_xxx_0.set_taps((firdes.complex_band_pass(1, self.rx_samp_rate, self.fL, self.fH, 100, firdes.WIN_HAMMING )))
        self.fft_filter_xxx_0_0.set_taps((firdes.complex_band_pass(1, self.rx_samp_rate, self.fL, self.fH, 100, firdes.WIN_HAMMING )))

    def get_addr(self):
        return self.addr

    def set_addr(self, addr):
        self.addr = addr


if __name__ == '__main__':
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    if gr.enable_realtime_scheduling() != gr.RT_OK:
        print "Error: failed to enable realtime scheduling."
    from distutils.version import StrictVersion
    if StrictVersion(Qt.qVersion()) >= StrictVersion("4.5.0"):
        Qt.QApplication.setGraphicsSystem(gr.prefs().get_string('qtgui','style','raster'))
    qapp = Qt.QApplication(sys.argv)
    tb = Red_Pitaya_digi_trx_USB()
    tb.start()
    tb.show()

    def quitting():
        tb.stop()
        tb.wait()
    qapp.connect(qapp, Qt.SIGNAL("aboutToQuit()"), quitting)
    qapp.exec_()
    tb = None  # to clean up Qt widgets
