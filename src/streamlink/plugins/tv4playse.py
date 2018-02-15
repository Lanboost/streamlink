"""
Plugin for Dplay service.

Trying to fix Dplay plugin, I have no plugin experiance therefore not very good...


API requests will be 400-bad request if not cookie['st'] is sent
st seems to be some sort of Akamai HD player verification
check hds.py _pv_params

HLS only uses either audio or video if not mixed by ffmpeg, am I doing something wrong?
(Sample .m3u8 applied at end of this file.

HDS dont find any playable streams, I have no clue why
sample find below (.mpd)
"""

import re
import time
import json
import urlparse

from streamlink.compat import quote
from streamlink.exceptions import PluginError, NoStreamsError
from streamlink.plugin import Plugin
from streamlink.plugin.api import StreamMapper, http, validate
from streamlink.stream import HLSStream, HDSStream
from streamlink.stream.ffmpegmux import FFMPEGMuxer, MuxedStream
# User-agent to use for http requests
USER_AGENT = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.82 Safari/537.36'
SWF_URL = 'http://player.{0}/4.3.5/swf/AkamaiAdvancedFlowplayerProvider_v3.8.swf'

# Regular expressions for matching URL and video ID
_url_re = re.compile(r'(?:http(s)?://)?www.tv4play.se/')



class tv4playse (Plugin):
	@classmethod
	def can_handle_url(cls, url):
		return _url_re.match(url)

	# Assembles available streams
	def _get_streams(self):
		print("This plugin is in DEVELOPMENT PHASE, USE AT OWN RISK!")
		print("For now only supports HLS with multistream")
		print("cookie is hardcoded, if not working try different cookie with name st")
		
		self.session.set_option("ffmpeg-ffmpeg", "D:/Downloads/ffmpeg.exe")
		
		if not FFMPEGMuxer.is_usable(self.session):
			print("Need ffmpegmuxer please set path to ffmpeg ")
			return False

		hdr = {'User-Agent': USER_AGENT.format('sv_SE')}

		#get the urldata for the path part of the url, needed in the api request
		urldata = urlparse.urlparse(self.url)
		id = urldata.path[urldata.path.rfind("/")+1:]
		
		#create the api url
		idurl = "https://playback-api.b17g.net/media/{0}?service=tv4&device=browser&protocol=dash%2C+hls&drm=widevine".format(id)
		res = http.get(idurl, headers=hdr)
		
		#fetch the manifest url
		
		#hls .m3u8 url
		playlisturl = json.loads(res.text)["playbackItem"]["manifestUrl"]
		
		#dash .mpd url
		#playlisturl = obj["data"]["attributes"]["streaming"]["dash"]["url"]
		
		ret = HLSStream.parse_variant_playlist(self.session,playlisturl)
		
		
		#ret = HDSStream.parse_manifest(self.session,playlisturl, is_akamai=True, headers=hdr, params={'hdcore': '3.8.0'},
		#						 pvswf=SWF_URL.format(self.domain))
		print(ret)
		return ret
		#return HDSStream.parse_manifest(self.session,playlisturl, headers=hdr)
		


__plugin__ = tv4playse






'''
Sample .m3u8 File


#EXTM3U
#EXT-X-VERSION:4
#EXT-X-INDEPENDENT-SEGMENTS
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="159992mp4a.40.2",LANGUAGE="und",NAME="und",AUTOSELECT=YES,DEFAULT=NO,CHANNELS="2",URI="1402891446-prog_index.m3u8?version_hash=9e734d85"
#EXT-X-MEDIA:TYPE=AUDIO,GROUP-ID="64000mp4a.40.2",LANGUAGE="und",NAME="und",AUTOSELECT=YES,DEFAULT=NO,CHANNELS="2",URI="1473243166-prog_index.m3u8?version_hash=9e734d85"
#EXT-X-MEDIA:TYPE=SUBTITLES,GROUP-ID="100wvtt.vtt",LANGUAGE="sv",NAME="sv",AUTOSELECT=YES,DEFAULT=NO,FORCED=NO,URI="1112635959-prog_index.m3u8?version_hash=9e734d85"
#EXT-X-STREAM-INF:BANDWIDTH=1751292,RESOLUTION=960x540,FRAME-RATE=25.000,CODECS="avc1.4D401F,mp4a.40.2",AUDIO="159992mp4a.40.2",SUBTITLES="100wvtt.vtt"
1798248473-prog_index.m3u8?version_hash=9e734d85
#EXT-X-STREAM-INF:BANDWIDTH=234268,RESOLUTION=320x180,FRAME-RATE=25.000,CODECS="avc1.42C015,mp4a.40.2",AUDIO="64000mp4a.40.2",SUBTITLES="100wvtt.vtt"
1090439967-prog_index.m3u8?version_hash=9e734d85
#EXT-X-STREAM-INF:BANDWIDTH=464188,RESOLUTION=480x270,FRAME-RATE=25.000,CODECS="avc1.42C01F,mp4a.40.2",AUDIO="64000mp4a.40.2",SUBTITLES="100wvtt.vtt"
823007626-prog_index.m3u8?version_hash=9e734d85
#EXT-X-STREAM-INF:BANDWIDTH=862228,RESOLUTION=640x360,FRAME-RATE=25.000,CODECS="avc1.4D401E,mp4a.40.2",AUDIO="64000mp4a.40.2",SUBTITLES="100wvtt.vtt"
40977015-prog_index.m3u8?version_hash=9e734d85
#EXT-X-STREAM-INF:BANDWIDTH=3339940,RESOLUTION=1280x720,FRAME-RATE=25.000,CODECS="avc1.64001F,mp4a.40.2",AUDIO="159992mp4a.40.2",SUBTITLES="100wvtt.vtt"
1140912457-prog_index.m3u8?version_hash=9e734d85
#EXT-X-STREAM-INF:BANDWIDTH=6533420,RESOLUTION=1920x1080,FRAME-RATE=25.000,CODECS="avc1.640029,mp4a.40.2",AUDIO="159992mp4a.40.2",SUBTITLES="100wvtt.vtt"
1453080601-prog_index.m3u8?version_hash=9e734d85
#EXT-X-STREAM-INF:BANDWIDTH=64100,CODECS="mp4a.40.2",AUDIO="64000mp4a.40.2",SUBTITLES="100wvtt.vtt"
1473243166-prog_index.m3u8?version_hash=9e734d85


#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=21271,RESOLUTION=320x180,CODECS="avc1.42C015",URI="1090439967-iframe.m3u8?version_hash=9e734d85"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=50011,RESOLUTION=480x270,CODECS="avc1.42C01F",URI="823007626-iframe.m3u8?version_hash=9e734d85"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=99766,RESOLUTION=640x360,CODECS="avc1.4D401E",URI="40977015-iframe.m3u8?version_hash=9e734d85"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=198900,RESOLUTION=960x540,CODECS="avc1.4D401F",URI="1798248473-iframe.m3u8?version_hash=9e734d85"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=397481,RESOLUTION=1280x720,CODECS="avc1.64001F",URI="1140912457-iframe.m3u8?version_hash=9e734d85"
#EXT-X-I-FRAME-STREAM-INF:BANDWIDTH=796666,RESOLUTION=1920x1080,CODECS="avc1.640029",URI="1453080601-iframe.m3u8?version_hash=9e734d85"
'''


'''
Sample .mpd file



<?xml version="1.0" encoding="UTF-8"?>
<MPD xmlns="urn:mpeg:dash:schema:mpd:2011" xmlns:cenc="urn:mpeg:cenc:2013" xmlns:mspr="urn:microsoft:playready" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:mpeg:dash:schema:mpd:2011 http://standards.iso.org/ittf/PubliclyAvailableStandards/MPEG-DASH_schema_files/DASH-MPD.xsd" profiles="urn:mpeg:dash:profile:isoff-live:2011,urn:com:dashif:dash264" minBufferTime="PT10S" type="static" mediaPresentationDuration="PT41M51.520S">
   <Period id="0" start="PT0S" duration="PT41M51.520S">
      <AdaptationSet group="0" mimeType="video/mp4" contentType="video" minBandwidth="170200" maxBandwidth="6370128" segmentAlignment="true" startWithSAP="1" minWidth="320" maxWidth="1920" minHeight="180" maxHeight="1080" maxFrameRate="25" par="16:9">
         <ContentProtection schemeIdUri="urn:mpeg:dash:mp4protection:2011" value="cenc" cenc:default_KID="416E6472-6561-7320-6572-2073746F7230" />
         <ContentProtection schemeIdUri="urn:uuid:1077efec-c0b2-4d02-ace3-3c1e52e2fb4b">
            <cenc:pssh>AAAANHBzc2gBAAAAEHfv7MCyTQKs4zweUuL7SwAAAAFBbmRyZWFzIGVyIHN0b3IwAAAAAA==</cenc:pssh>
         </ContentProtection>
         <SegmentTemplate timescale="90000" initialization="$RepresentationID$-init?hdntl=exp=1518182366~acl=/*~data=hdntl~hmac=3499c9c4fbe22a7f50ccecca4b5711b6fc969b1bb1e054c818e37a67eb3951ca&amp;version_hash=1a0f1faf" media="$RepresentationID$-$Time$?hdntl=exp=1518182366~acl=/*~data=hdntl~hmac=3499c9c4fbe22a7f50ccecca4b5711b6fc969b1bb1e054c818e37a67eb3951ca&amp;version_hash=1a0f1faf" presentationTimeOffset="0">
            <SegmentTimeline>
               <S d="180000" t="0" />
               <S d="180000" r="1253" />
               <S d="136800" />
            </SegmentTimeline>
         </SegmentTemplate>
         <Representation id="1779133779" bandwidth="1592096" codecs="avc1.4D401F" width="960" height="540" frameRate="25" sar="1:1" />
         <Representation id="1020176500" bandwidth="170200" codecs="avc1.42C015" width="320" height="180" frameRate="25" sar="1:1" />
         <Representation id="1829817257" bandwidth="400176" codecs="avc1.42C01F" width="480" height="270" frameRate="25" sar="1:1" />
         <Representation id="116106584" bandwidth="798288" codecs="avc1.4D401E" width="640" height="360" frameRate="25" sar="1:1" />
         <Representation id="1456331626" bandwidth="3182808" codecs="avc1.64001F" width="1280" height="720" frameRate="25" sar="1:1" />
         <Representation id="2104417298" bandwidth="6370128" codecs="avc1.640029" width="1920" height="1080" frameRate="25" sar="1:1" />
      </AdaptationSet>
      <AdaptationSet group="1" mimeType="audio/mp4" contentType="audio" minBandwidth="64000" maxBandwidth="159992" segmentAlignment="true" startWithSAP="1" lang="und">
         <ContentProtection schemeIdUri="urn:mpeg:dash:mp4protection:2011" value="cenc" cenc:default_KID="416E6472-6561-7320-6572-2073746F7230" />
         <ContentProtection schemeIdUri="urn:uuid:1077efec-c0b2-4d02-ace3-3c1e52e2fb4b">
            <cenc:pssh>AAAANHBzc2gBAAAAEHfv7MCyTQKs4zweUuL7SwAAAAFBbmRyZWFzIGVyIHN0b3IwAAAAAA==</cenc:pssh>
         </ContentProtection>
         <SegmentTemplate timescale="90000" initialization="$RepresentationID$-init?hdntl=exp=1518182366~acl=/*~data=hdntl~hmac=3499c9c4fbe22a7f50ccecca4b5711b6fc969b1bb1e054c818e37a67eb3951ca&amp;version_hash=1a0f1faf" media="$RepresentationID$-$Time$?hdntl=exp=1518182366~acl=/*~data=hdntl~hmac=3499c9c4fbe22a7f50ccecca4b5711b6fc969b1bb1e054c818e37a67eb3951ca&amp;version_hash=1a0f1faf" presentationTimeOffset="0">
            <SegmentTimeline>
               <S d="172800" t="0" />
               <S d="172800" r="1306" />
               <S d="28800" />
            </SegmentTimeline>
         </SegmentTemplate>
         <Representation id="1473243166" bandwidth="64000" codecs="mp4a.40.2" audioSamplingRate="48000" />
         <Representation id="1402891446" bandwidth="159992" codecs="mp4a.40.2" audioSamplingRate="48000" />
      </AdaptationSet>
      <AdaptationSet group="2" mimeType="text/vtt" contentType="text" lang="sv">
         <Representation id="1112635959" bandwidth="100">
            <BaseURL>1112635959-0.vtt?hdntl=exp=1518182366~acl=/*~data=hdntl~hmac=3499c9c4fbe22a7f50ccecca4b5711b6fc969b1bb1e054c818e37a67eb3951ca&amp;version_hash=1a0f1faf</BaseURL>
         </Representation>
      </AdaptationSet>
   </Period>
</MPD>
'''