from enigma import eDVBResourceManager, Misc_Options, eDVBCIInterfaces
from Tools.Directories import fileExists, fileCheck, pathExists, fileHas
from Tools.HardwareInfo import HardwareInfo
from Components.About import getChipSetString

from boxbranding import getMachineBuild, getBoxType, getBrandOEM, getDisplayType, getHaveRCA, getHaveYUV, getHaveSCART, getHaveAVJACK, getHaveHDMIinHD, getHaveHDMIinFHD, getMachineMtdRoot

SystemInfo = { }

#FIXMEE...
def getNumVideoDecoders():
	idx = 0
	while fileExists("/dev/dvb/adapter0/video%d"% idx, 'f'):
		idx += 1
	return idx

def countFrontpanelLEDs():
	leds = 0
	if fileExists("/proc/stb/fp/led_set_pattern"):
		leds += 1
	while fileExists("/proc/stb/fp/led%d_pattern" % leds):
		leds += 1
	return leds

SystemInfo["CommonInterface"] = eDVBCIInterfaces.getInstance().getNumOfSlots()
SystemInfo["CommonInterfaceCIDelay"] = fileCheck("/proc/stb/tsmux/rmx_delay")
for cislot in range (0, SystemInfo["CommonInterface"]):
	SystemInfo["CI%dSupportsHighBitrates" % cislot] = fileCheck("/proc/stb/tsmux/ci%d_tsclk"  % cislot)
	SystemInfo["CI%dRelevantPidsRoutingSupport" % cislot] = fileCheck("/proc/stb/tsmux/ci%d_relevant_pids_routing"  % cislot)

SystemInfo["NumVideoDecoders"] = getNumVideoDecoders()
SystemInfo["PIPAvailable"] = SystemInfo["NumVideoDecoders"] > 1
SystemInfo["CanMeasureFrontendInputPower"] = eDVBResourceManager.getInstance().canMeasureFrontendInputPower()
SystemInfo["12V_Output"] = Misc_Options.getInstance().detected_12V_output()
SystemInfo["FrontpanelDisplay"] = fileExists("/dev/dbox/oled0") or fileExists("/dev/dbox/lcd0")
SystemInfo["7segment"] = getDisplayType() in ('7segment')
SystemInfo["ConfigDisplay"] = SystemInfo["FrontpanelDisplay"] and getDisplayType() not in ('7segment')
SystemInfo["LCDSKINSetup"] = pathExists("/usr/share/enigma2/display") and not SystemInfo["7segment"]
SystemInfo["ZapMode"] = fileCheck("/proc/stb/video/zapmode") or fileCheck("/proc/stb/video/zapping_mode")
SystemInfo["NumFrontpanelLEDs"] = countFrontpanelLEDs()
SystemInfo["OledDisplay"] = fileExists("/dev/dbox/oled0")
SystemInfo["LcdDisplay"] = fileExists("/dev/dbox/lcd0")
SystemInfo["DisplayLED"] = False
SystemInfo["LEDButtons"] = getBoxType() == 'vuultimo'
SystemInfo["DeepstandbySupport"] = HardwareInfo().has_deepstandby()
SystemInfo["Fan"] = fileCheck("/proc/stb/fp/fan")
SystemInfo["FanPWM"] = SystemInfo["Fan"] and fileCheck("/proc/stb/fp/fan_pwm")
SystemInfo["PowerLed"] = False
SystemInfo["StandbyLED"] = False
SystemInfo["SuspendLED"] = False
SystemInfo["LedPowerColor"] = False
SystemInfo["LedStandbyColor"] = False
SystemInfo["LedSuspendColor"] = False
SystemInfo["Power4x7On"] = False
SystemInfo["Power4x7Standby"] = False
SystemInfo["Power4x7Suspend"] = False
SystemInfo["WakeOnLAN"] = fileCheck("/proc/stb/power/wol") or fileCheck("/proc/stb/fp/wol")
SystemInfo["HDMICEC"] = (fileExists("/dev/hdmi_cec") or fileExists("/dev/misc/hdmi_cec0")) and fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/HdmiCEC/plugin.pyo")
SystemInfo["SABSetup"] = fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/SABnzbd/plugin.pyo")
SystemInfo["Blindscan"] = fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/Blindscan/plugin.pyo")
SystemInfo["Satfinder"] = fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/Satfinder/plugin.pyo")
SystemInfo["HasExternalPIP"] = fileCheck("/proc/stb/vmpeg/1/external")
SystemInfo["VideoDestinationConfigurable"] = fileExists("/proc/stb/vmpeg/0/dst_left")
SystemInfo["hasPIPVisibleProc"] = fileCheck("/proc/stb/vmpeg/1/visible")
SystemInfo["VFD_scroll_repeats"] = not SystemInfo["7segment"] and fileCheck("/proc/stb/lcd/scroll_repeats")
SystemInfo["VFD_scroll_delay"] = not SystemInfo["7segment"] and fileCheck("/proc/stb/lcd/scroll_delay")
SystemInfo["VFD_initial_scroll_delay"] = not SystemInfo["7segment"] and fileCheck("/proc/stb/lcd/initial_scroll_delay")
SystemInfo["VFD_final_scroll_delay"] = not SystemInfo["7segment"] and fileCheck("/proc/stb/lcd/final_scroll_delay")
SystemInfo["LcdLiveTV"] = fileCheck("/proc/stb/fb/sd_detach") or fileCheck("/proc/stb/lcd/live_enable")
SystemInfo["LCDMiniTV"] = fileExists("/proc/stb/lcd/mode")
SystemInfo["LCDMiniTVPiP"] = SystemInfo["LCDMiniTV"]
SystemInfo["LcdPowerOn"] = fileExists("/proc/stb/power/vfd")
SystemInfo["FastChannelChange"] = False
SystemInfo["3DMode"] = fileCheck("/proc/stb/fb/3dmode") or fileCheck("/proc/stb/fb/primary/3d")
SystemInfo["3DZNorm"] = fileCheck("/proc/stb/fb/znorm") or fileCheck("/proc/stb/fb/primary/zoffset")
SystemInfo["Blindscan_t2_available"] = fileCheck("/proc/stb/info/vumodel")
SystemInfo["HasTranscoding"] = pathExists("/proc/stb/encoder/0") or fileCheck("/dev/bcm_enc0")
SystemInfo["HasH265Encoder"] = fileHas("/proc/stb/encoder/0/vcodec_choices", "h265")
SystemInfo["CanNotDoSimultaneousTranscodeAndPIP"] = getBoxType() in ('vusolo4k')
SystemInfo["hasXcoreVFD"] = fileCheck("/sys/module/brcmstb_%s/parameters/pt6302_cgram" % getBoxType())
SystemInfo["HasHDMIin"] = getHaveHDMIinHD() in ('True',) or getHaveHDMIinFHD() in ('True',)
SystemInfo["HasHDMI-CEC"] = fileExists("/usr/lib/enigma2/python/Plugins/SystemPlugins/HdmiCEC/plugin.pyo")
SystemInfo["HasInfoButton"] = False
SystemInfo["Has24hz"] = fileCheck("/proc/stb/video/videomode_24hz")
SystemInfo["HasRootSubdir"] = False
SystemInfo["RecoveryMode"] = False
SystemInfo["canMultiBoot"] = False
SystemInfo["canBackupEMC"] = False
SystemInfo["HasHiSi"] = False
SystemInfo["canMode12"] = False
SystemInfo["HasMMC"] = False
SystemInfo["HasSDmmc"] = False
SystemInfo["HasH9SD"] = False
SystemInfo["CanProc"] = False
SystemInfo["Canaudiosource"] = fileCheck("/proc/stb/hdmi/audio_source")
SystemInfo["Can3DSurround"] = fileHas("/proc/stb/audio/3d_surround_choices", "none")
SystemInfo["Can3DSpeaker"] = fileHas("/proc/stb/audio/3d_surround_speaker_position_choices", "center")
SystemInfo["CanAutoVolume"] = fileHas("/proc/stb/audio/avl_choices", "none")
SystemInfo["supportPcmMultichannel"] = fileCheck("/proc/stb/audio/multichannel_pcm")
SystemInfo["CanDownmixAC3"] = fileHas("/proc/stb/audio/ac3_choices", "downmix")
SystemInfo["CanAC3Transcode"] = fileHas("/proc/stb/audio/ac3plus_choices", "force_ac3")
SystemInfo["CanDownmixDTS"] = fileHas("/proc/stb/audio/dts_choices", "downmix")
SystemInfo["CanDTSHD"] = fileHas("/proc/stb/audio/dtshd_choices", "downmix")
SystemInfo["CanDownmixAAC"] = fileHas("/proc/stb/audio/aac_choices", "downmix")
SystemInfo["CanDownmixAACPlus"] = fileHas("/proc/stb/audio/aacplus_choices", "downmix")
SystemInfo["CanAACTranscode"] = fileHas("/proc/stb/audio/aac_transcode_choices", "off")
SystemInfo["CanWMAPRO"] = fileHas("/proc/stb/audio/wmapro_choices", "downmix")
SystemInfo["havecolorspace"] = fileCheck("/proc/stb/video/hdmi_colorspace")
SystemInfo["havecolorspacechoices"] = fileCheck("/proc/stb/video/hdmi_colorspace_choices")
SystemInfo["havecolorimetry"] = fileCheck("/proc/stb/video/hdmi_colorimetry")
SystemInfo["havecolorimetrychoices"] = fileCheck("/proc/stb/video/hdmi_colorimetry_choices")
SystemInfo["havehdmicolordepth"] = fileCheck("/proc/stb/video/hdmi_colordepth")
SystemInfo["havehdmicolordepthchoices"] = fileCheck("/proc/stb/video/hdmi_colordepth_choices")
SystemInfo["havehdmihdrtype"] = fileExists("/proc/stb/video/hdmi_hdrtype")
SystemInfo["HDRSupport"] = fileExists("/proc/stb/hdmi/hlg_support_choices")
SystemInfo["Canedidchecking"] = fileCheck("/proc/stb/hdmi/bypass_edid_checking")
SystemInfo["haveboxmode"] = fileExists("/proc/stb/info/boxmode")
SystemInfo["HasScaler_sharpness"] = pathExists("/proc/stb/vmpeg/0/pep_scaler_sharpness")
# Machines that do have SCART component video (red, green and blue RCA sockets).
SystemInfo["Scart-YPbPr"] = getBrandOEM() == "vuplus" and not "4k" in getBoxType()
# Machines that do not have component video (red, green and blue RCA sockets).
SystemInfo["no_YPbPr"] = getHaveYUV() in ('False',)
# Machines that have composite video (yellow RCA socket) but do not have Scart.
SystemInfo["yellow_RCA_no_scart"] = getHaveSCART() in ('False',) and (getHaveRCA() in ('True',) or getHaveAVJACK() in ('True',))
# Machines that have neither yellow RCA nor Scart sockets
SystemInfo["no_yellow_RCA__no_scart"] = getHaveRCA() in ('False',) and (getHaveSCART() in ('False',) and getHaveAVJACK() in ('False',))
SystemInfo["VideoModes"] = getChipSetString() in ( # 2160p and 1080p capable hardware
		'5272s', '7251', '7251s', '7252', '7252s', '72604', '7278', '7366', '7376', '7444s'
	) and (
		["720p", "1080p", "2160p", "2160p30", "1080i", "576p", "576i", "480p", "480i"], # normal modes
		{"720p", "1080p", "2160p", "2160p30", "1080i"} # widescreen modes
	) or getChipSetString() in ( # 1080p capable hardware
		'7241', '7356', '73565', '7358', '7362', '73625', '7424', '7425', '7552'
	) and (
		["720p", "1080p", "1080i", "576p", "576i", "480p", "480i"], # normal modes
		{"720p", "1080p", "1080i"} # widescreen modes
	) or ( # default modes (neither 2160p nor 1080p capable hardware)
		["720p", "1080i", "576p", "576i", "480p", "480i"], # normal modes
		{"720p", "1080i"} # widescreen modes
	)
