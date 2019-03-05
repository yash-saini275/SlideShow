import sys

sys.setrecursionlimit(1500)

class Photo(object):
    """Class which contains information about the Photos their orientation, numbers of tags,
    list of tags"""
    def __init__(self, line):
        self.direction = line[0]
        self.integer = int(line[1])
        self.tags = line[2: ]

    def __str__(self):
        out = self.direction + ' ' + str(self.integer) + ' ' + str(self.tags)
        return out

class Slide(object):
    """Slide class contains the information about one slide the list of photos one slide contains
   and the list of tags"""
    def __init__(self, tags):
        self.photos = []
        self.tags = set(tags)

    def __str__(self):
        out = str(self.photos) + ' ' + str(self.tags)
        return out

class SlideShow(object):
    """SlideShow class contains the list of class, photos. Slides list contains the list of slides 
    in order of the slide show."""
    def __init__(self, N):
        self.numberOfPhotos = int(N)
        self.photos = []
        self.horizontalPhotos = []
        self.verticalPhotos = []
        self.slides = []
        self.slideShow = []

    def splitPhotos(self):
        """splitPhotos function seperates the photos according to their orientation in seperate lists."""
        for number in range(self.numberOfPhotos):
            if self.photos[number].direction == 'H':
                self.horizontalPhotos.append(number)
            if self.photos[number].direction == 'V':
                self.verticalPhotos.append(number)

    def makeSlide(self):
        """makeSlide function makes the Slide from photos list."""
        for index in self.horizontalPhotos:
            self.slides.append(Slide(self.photos[index].tags))
            self.slides[-1].photos.append(index)

        for index in range(0, len(self.verticalPhotos) - 1, 2):
            self.slides.append(Slide(self.photos[self.verticalPhotos[index]].tags))
            for tag in self.photos[self.verticalPhotos[index + 1]].tags:
                self.slides[-1].tags.add(tag)
            self.slides[-1].photos.append(self.verticalPhotos[index])
            self.slides[-1].photos.append(self.verticalPhotos[index + 1])

    
#def makeInterestingSlideShow(horizontalPhotos, verticalPhotos):
#    slideShow = []

#    pass

def mergeSort(listOfSlides):
    if len(listOfSlides) == 1 or len(listOfSlides) == 0:
        return listOfSlides
    
    leftSubList = mergeSort(listOfSlides[0 : int(len(listOfSlides) / 2) ])
    rightSubList = mergeSort(listOfSlides[int(len(listOfSlides) / 2): ])

    return Merge(leftSubList, rightSubList)

def Merge(leftSubList, rightSubList):
    """This is the merge sort algorithm used to sort slides accorging to the scoring"""
    mergedList = []
    leftIndex = 0
    rightIndex = 0
    if len(leftSubList) > len(rightSubList):
        while leftIndex <= len(leftSubList):
            if len(mergedList) == 0:
                mergedList.append(leftSubList[leftIndex])
                leftIndex += 1
            else:
                try:
                    if findScore(mergedList[-1], leftSubList[leftIndex]) > findScore(mergedList[-1], leftSubList[rightIndex]):
                        mergedList.append(leftSubList[leftIndex])
                        leftIndex += 1
                    else:
                        mergedList.append(rightSubList[rightIndex])
                        rightIndex += 1
                except IndexError:
                    if rightIndex == len(rightSubList):
                        for slide in leftSubList[leftIndex:]:
                            mergedList.append(slide)
                        return mergedList
                    else:
                        for slide in rightSubList[rightIndex:]:
                            mergedList.append(slide)
                        return mergedList
    else:
        while rightIndex <= len(rightSubList):
            if len(mergedList) == 0:
                mergedList.append(rightSubList[rightIndex])
                rightIndex += 1
            else:
                try:
                    if findScore(mergedList[-1], leftSubList[leftIndex]) > findScore(mergedList[-1], rightSubList[rightIndex]):
                        mergedList.append(leftSubList[leftIndex])
                        leftIndex += 1
                    else:
                        mergedList.append(rightSubList[rightIndex])
                        rightIndex += 1
                except IndexError:
                    if rightIndex == len(rightSubList):
                        for slide in leftSubList[leftIndex: ]:
                            mergedList.append(slide)
                        return mergedList
                    else:
                        for slide in rightSubList[rightIndex: ]:
                            mergedList.append(slide)
                        return mergedList
    return mergedList

def findScore(slide1: Slide, slide2: Slide):
    return min(len(set.intersection(slide1.tags, slide2.tags)), len(set.difference(slide1.tags, slide2.tags)), len(set.difference(slide2.tags, slide1.tags)))

def makeOutput(filenmae, slideShow):
    """makeOutput function makes the output file """
    outputFileName = filename[:-4] + '_output.txt'
    fopen = open(outputFileName, 'w')
    fopen.write(str(len(slideShow.slideShow)))
    for numOfSlides in range(len(slideShow.slideShow)):
        fopen.write('\n')
        for photoId in slideShow.slideShow[numOfSlides].photos:
            fopen.write(str(photoId))
            fopen.write(' ')
        


def makeSlideShow(filename):
    """makeSlideShow is the main fucntion which makes the slide show."""
    with open(filename, 'r') as fi:
        show = SlideShow(fi.readline())
        for _ in range(show.numberOfPhotos):
            show.photos.append(Photo(fi.readline().split()))

        show.splitPhotos()
        show.makeSlide()
        #show.rearrangeSlides()
        show.slideShow = mergeSort(show.slides)

        makeOutput(filename, show)


filename = input()
makeSlideShow(filename)