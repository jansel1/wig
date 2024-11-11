# Wait Interface Generator (WIG)

Create modern loading screens for applications, programs, anything. Theres not much to explain here, it's very simple and really requires less than 30s to make a good looking loading screen. 

## Code Example

```python
    import wig

    loadingScreen = wig.AddLoadingScreen(image | str, dimensions | int tuple, draggable | bool, cursor | str, 
                                        fadein | bool, fadein_delayms | int)

    loadingScreen.ChangeCursor("tkinter-cursor") # Change cursor (must be a TKinter cursor)
    loadingScreen.Destroy() # Destroy window

    # image argument example: "path/to/image.jpg"
    # dimensions argument example: (800, 500) (X and Y)
    # draggable argument example: true
    # cursor argument example: "arrow"
    # fadein argument example: true
    # fadein_delayms example: 10
    
```

You can also spam press control to exit the loading screen at any moment in case of failure. 

## Known Issues

- As of now, WIG can't handle more than one screen PER program.

