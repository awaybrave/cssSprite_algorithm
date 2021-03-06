import pdb
class ImageDealer:
	def readImageInfo(self, path):
		# read a path 
		return None
	def outputEnclosingImage(self, enInfo):
		return None	

class RectanglesEnclosing:
	def __init__(self, rects):
		self.rects = rects
		self.rectsTotal = 0
		self.maxWidth = 0;
		for rect in rects:
			self.rectsTotal = self.rectsTotal + rect['width'] * rect['height']
			self.maxWidth = max(self.maxWidth, rect['width'])
		self.eresult = {}
	def setSize(self, width, height):
		self.ew = width
		self.eh = height
	def computeEnclosing(self):
		occupied = [[False]]
		rowHeight = [self.eh]
		colWidth = [self.ew]
		rectPosition = []
		failedRect = None
		rightMostRect = 0 
		rightMostPos = 0
		rightMostTallest = 0
		bottomMostPos = 0
		for rect in self.rects:
			rectPlaced = False
			for col in range(0, len(occupied)):
				gotSpace = False
				for row in range(0, len(occupied[col])): 
					if not occupied[col][row]:
						# check height of rows
						targetRows = []
						i = row
						curHeight = 0
						while curHeight < rect['height'] and i < len(rowHeight):
							if not occupied[col][i]:
								curHeight = curHeight + rowHeight[i]
								targetRows.append(i)
								i = i + 1
							else:
								break
						if curHeight >= rect['height']:
							# check width of cols
							targetCols = []
							j = col
							curWidth = 0
							while curWidth < rect['width'] and j < len(colWidth):
								if not occupied[j][row]:
									curWidth = curWidth + colWidth[j]
									targetCols.append(j)
									j = j + 1
								else:
									break
							if curWidth >= rect['width']:
								# check the combination of targetRows and targetCols
								flag = True 
								for tc in targetCols:
									for tr in targetRows:
										if occupied[tc][tr]:
											flag = False
											break
									if not flag:
										break
								if flag:
									if curWidth > rect['width']:
										# split the last col into two
										insertColPos = targetCols[-1]+1
										overWidth = curWidth - rect['width']
										colWidth[insertColPos-1] = colWidth[insertColPos-1] - overWidth
										colWidth.insert(insertColPos, overWidth)
										occupied.insert(insertColPos, [False]*len(rowHeight))
									if curHeight > rect['height']:
										# split the last row into two
										insertRowPos = targetRows[-1]+1
										overHeight = curHeight - rect['height']
										rowHeight[insertRowPos-1] = rowHeight[insertRowPos-1] - overHeight
										rowHeight.insert(insertRowPos, overHeight)
										for c in range(len(occupied)):
											if c >= targetCols[0] and c <= targetCols[-1]: 
												occupied[c].insert(insertRowPos, False)	
											else:
												occupied[c].insert(insertRowPos, occupied[c][insertRowPos-1])
									for tc in targetCols:
										for tr in targetRows:
											occupied[tc][tr] = True
									startRow = targetRows[0]
									startCol = targetCols[0]
									rowPos = 0
									colPos = 0
									for r in range(0, startRow):
										rowPos = rowPos + rowHeight[r]	
									for c in range(0, startCol):
										colPos = colPos + colWidth[c]
									rectPosition.append({'x': colPos, 'y': rowPos})
									gotSpace = True
									break
				if gotSpace:
					rightPos = rectPosition[-1]['x'] + rect['width']
					bottomPos = rectPosition[-1]['y'] + rect['height']
					if rightMostPos < rightPos or rightMostPos == rightPos and rect['height'] > rightMostRect['height']:
						rightMostPos = rightPos
						rightMostRect = rect
						rightMostTallest = rect['height']

					if bottomMostPos < bottomPos:
						bottomMostPos = bottomPos
					rectPlaced = True
					break
			if not rectPlaced:
				failedRect = rect	
				break
		#print occupied
		#print rowHeight
		#print colWidth
		#print rectPosition
		if len(rectPosition) < len(self.rects):
			return {'result': False, 'failedRect': failedRect, 'size': {'width': self.ew, 'height': self.eh}}
		else:
			return {
					'result': True, 'rightMostRect': rightMostRect, 
					'size': {'width': rightMostPos, 'height': bottomMostPos, 'area': rightMostPos * bottomMostPos}, 
					'rectPosition': rectPosition
				} 

	def compute(self):
		successCount = 0
		while self.ew >= self.maxWidth:
			#pdb.set_trace()
			computeResult = self.computeEnclosing()
			if computeResult['result']:
				if not self.eresult:
					self.eresult = computeResult
				else:
					#pdb.set_trace()
					if self.eresult['size']['area'] > computeResult['size']['area']: 
						self.eresult = computeResult
				successCount = successCount + 1
				if successCount == 10:
					break
				newWidth = computeResult['size']['width']-1
				newHeight = computeResult['size']['height']+computeResult['rightMostRect']['height']
				while newWidth * newHeight < self.rectsTotal:
					newHeight = newHeight + 1
			else: 
				newWidth = self.eresult['size']['width']-1
				newHeight = computeResult['size']['height'] + computeResult['failedRect']['height']
			self.setSize(newWidth, newHeight)
		print (self.rectsTotal)
		print (self.eresult['size']['area'])
		return self.eresult

def main():
	# init work: input rectangles , sort them by
	# their height, greatest height first,
	# and set the up-boundary of the enclosing rectangle.

	inputs = open("input1.txt", "r")
	rectangles = []
	ewidth = 0
	eheight = 0
	for line in inputs:
		t = line.split(' ')		
		rectangles.append({
			'width': int(t[0]),
			'height': int(t[1])
		})
		ewidth = ewidth + int(t[0])
	rects = sorted(rectangles, key=lambda r: -r['height'])
	eheight = rects[0]['height']
	# end of init work
	
	# place the rectangles into the initial large rectangle
	action = RectanglesEnclosing(rects)
	action.setSize(ewidth, eheight)
	result = action.compute()

if __name__ == "__main__":
	main()
