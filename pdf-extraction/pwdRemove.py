import pikepdf

mypdf=pikepdf.open('20200709_PROCEDUREMRI-BRAIN-WITHOUT-CONTRAS.pdf', '07-04-2000-CSL')

mypdf.save('20200709_PROCEDUREMRI-BRAIN-WITHOUT-CONTRAS-unencrypted.pdf')