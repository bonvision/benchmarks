try
    AssertOpenGL;

    % Get the list of screens and choose the one with the highest screen number.
    screenNumber=max(Screen('Screens'));

    % Find the color values which correspond to white and black.
    white=WhiteIndex(screenNumber);
    black=BlackIndex(screenNumber);

    % Round gray to integral number, to avoid roundoff artifacts with some
    % graphics cards:
    gray=round((white+black)/2);
    inc=white-gray;
    
    % Open a double buffered fullscreen window with a gray background:
    w =Screen('OpenWindow',screenNumber, gray);

    % Make sure this GPU supports shading at all:
    AssertGLSL;
    
    % Get size of window
    [width, height] = Screen('WindowSize', w);
    
    % Enable alpha blending for typical drawing of masked textures:
    Screen('BlendFunction', w, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    % Query duration of monitor refresh interval:
    ifi=Screen('GetFlipInterval', w);

    waitframes = 1;
    waitduration = waitframes * ifi;
    
    % Perform initial Flip to sync us to the VBL and for getting an initial
    % VBL-Timestamp for our "WaitBlanking" emulation:
    vbl = Screen('Flip', w);
    
    % Run through all benchmark grid sizes
    spaceKey = KbName('space');
    for gridsize = 1:1000

        % Black loop: Run until space key is pressed.
        while 1
            [a,b,keyDown] = KbCheck;
            if any(keyDown(spaceKey))
                break
            end
            
            colour = 0;
            Screen('FillRect', w, colour, [0 0 width height]);
            
            % Flip 'wa itframes' monitor refresh intervals after last redraw.
            vbl = Screen('Flip', w, vbl + (waitframes - 0.5) * ifi);
        end
        
        % White loop: Run until space key is released.
        while 1
            [a,b,keyDown] = KbCheck;
            if ~any(keyDown(spaceKey))
                break
            end
            
            colour = 255;
            Screen('FillRect', w, colour, [0 0 width height]);
            
            % Flip 'waitframes' monitor refresh intervals after last redraw.
            vbl = Screen('Flip', w, vbl + (waitframes - 0.5) * ifi);
        end
    end
    
    % The same commands which close onscreen and offscreen windows also close textures.
    sca;
catch 
    % This "catch" section executes in case of an error in the "try" section
    % above. Importantly, it closes the onscreen window if it is open.
    sca;
    psychrethrow(apsychlasterror);

end %try..catch..
