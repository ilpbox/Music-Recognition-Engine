import web
import model
import numpy
import os
import uuid

from Queue import PriorityQueue

from pyAudioAnalysis import audioBasicIO
from pyAudioAnalysis import audioFeatureExtraction

urls = (
    '/', 'Index',
    '/results', 'ResultView',
    '/upload', 'Upload'
)

t_globals = {
    'datestr': web.datestr
}
render = web.template.render('templates', base='base', globals=t_globals)

class Index:
    def GET(self):
        return render.index()

class Upload:
    def POST(self):
        x = web.input(myfile={})
        filename = 'tmp/'+uuid.uuid4().hex+'.wav'
        file = open(filename, 'w+')
        file.seek(0)
        file.write(x['myfile'].value)
        file.close()
        [Fs, x] = audioBasicIO.readAudioFile(filename);
        #os.remove(filename)
        x = audioBasicIO.stereo2mono(x)
        [F, _] = audioFeatureExtraction.mtFeatureExtraction(x, Fs, round(Fs*1.0), round(Fs * 1.0), round(Fs * 0.050), round(Fs * 0.050))
        F = F.transpose()
        for vec in F:
            results={}
            current_highest = ""
            current_highest_value = 0
            vec = numpy.around(vec.astype(numpy.float), 6)
            current = model.getNN(vec)
            result = current[0][1].partition("_")[0]
            if result in results:
                results[result] = results[result]+1
            else:
                results[result] = 1
            if results[result] > current_highest_value:
                current_highest_value = results[result]
                current_highest = result
        print results
        print current_highest
        raise web.seeother('/')

class Sorch(web.application):
    def run(self, port=9898, *middleware):
        func = self.wsgifunc(*middleware)
        return web.httpserver.runsimple(func, ('0.0.0.0', port))

if __name__ == "__main__":
   app = Sorch(urls, globals()) 
   app.run()