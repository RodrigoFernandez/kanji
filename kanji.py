# -*- coding: utf-8 -*-

# Hecho en base a las extensiones listadas en: https://github.com/getnikola/nikola/tree/master/nikola/plugins/compile/rest
# tambien mirar: https://getnikola.com/extending.html#restextension-plugins
# https://elblogdehumitos.com/posts/nikola-un-proyecto-comunitario/
# http://darobin.github.io/html-ruby/

"""kanji directive for reStructuredText."""

from docutils import nodes
from docutils.parsers.rst import Directive, directives

from nikola.plugin_categories import RestExtension

class Plugin(RestExtension):
	"""Plugin for reST kanji directive."""
	
	name = "rest_kanji"
	
	def set_site(self, site):
		"""Set Nikola site."""
		self.site = site
		directives.register_directive('kanji', Kanji)
		self.site.register_shortcode('kanji', get_ruby_shortcode)
		Kanji.site = site
		return super(Plugin, self).set_site(site)

def get_ruby_shortcode(data=None, post=None, site=None, furigana=None, lang=None):
	"""Provide a reStructuredText directive to create kanji with furigana.
	
	Usage:
		
		.. kanji:: 日 本 語
			:furigana: に ほん ご
	
	Or:
		{{% kanji furigana=に|ほん|ご %}}日 本 語{{% /kanji %}}
	"""
	return get_ruby(data.split(" "), furiganas=furigana.replace('|', ' ')), []
	
def get_ruby(kanjis=[], furiganas=""):
	kanjis_list = kanjis
	furiganas_list = furiganas.split(' ')
	
	cantidad_asociaciones = min(len(kanjis_list), len(furiganas_list))
	i = 0
	aux = []
	while i < cantidad_asociaciones:
		aux.append('%s<rt>%s</rt>' % (kanjis_list[i], furiganas_list[i]))
		i = i + 1
	return '<ruby>' + "".join(aux) + '</ruby>'

class Kanji(Directive):
	"""Provide a reStructuredText directive to create kanji with furigana.
	
	Usage:
		.. kanji:: 日 本 語
			:furigana: に ほん ご
	
	"""
	
	has_content = True
	required_arguments = 1
	optional_arguments = 999
	option_spec = {
		'furigana': directives.unchanged
	}
	
	#<ruby>日<rt>に</rt></ruby>
	ruby_html = '<ruby>%s<rt>%s</rt></ruby>'
	
	def run(self):
		"""Run kanji directive."""
		return [nodes.raw('', get_ruby(self.arguments, self.options.get('furigana')), format='html')]
