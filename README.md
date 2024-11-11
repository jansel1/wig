# Wait Interface Generator (WIG)

Create modern loading screens for applications, programs, anything. Theres not much to explain here, it's very simple and really requires less than 30s to make a good looking loading screen. 

## Code Example

```python
    import wig

    loadingScreen = wig.AddLoadingScreen(image | str, dimensions | int tuple, draggable | bool, cursor | str, 
                                        fadein | bool, fadein_delayms | int)

    loadingScreen.ChangeCursor("tkinter-cursor") # Change cursor (must be a TKinter cursor)
    loadingScreen.Destroy() # Destroy window
```

(image must be some sort of path e.g. 'path/to/image.jpeg')

## Known Issues

As of now, WIG can't handle more than one screen PER program.