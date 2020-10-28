function Ensure-Video {
    param
	(
	    $FileName
	)
	
	if (!(Test-Path $FileName)) {
	    $url = "https://download.blender.org/durian/trailer/" + $FileName
		Invoke-WebRequest $url -OutFile $FileName
	}	
}

Ensure-Video -FileName "sintel_trailer-480p.ogv"
Ensure-Video -FileName "sintel_trailer-720p.ogv"
Ensure-Video -FileName "sintel_trailer-1080p.ogv"