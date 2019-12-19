blankDurationSecs=2; % Start with blank for 2 seconds.
movieDurationSecs=3; % Abort trial after 3 seconds.
texsize=100; % Half-Size of the grating image.
f=0.02; % Grating cycles/pixel
cyclespersecond=1; % Speed of grating in cycles per second
angle=0; % Angle of grating
gridsizes = 2.^[1:8]; % Benchmark grid sizes
    
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
    inc = floor((white-black)/2);
    
    % Open a double buffered fullscreen window with a gray background:
    w =Screen('OpenWindow',screenNumber, gray);

    % Make sure this GPU supports shading at all:
    AssertGLSL;
    
    % Get size of window
    [width, height] = Screen('WindowSize', w);
    
    % Enable alpha blending for typical drawing of masked textures:
    Screen('BlendFunction', w, GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA);

    % Create a special texture drawing shader for masked texture drawing:
    glsl = MakeTextureDrawShader(w, 'SeparateAlphaChannel');

    % Calculate parameters of the grating:
    p=ceil(1/f); % pixels/cycle, rounded up.
    fr=f*2*pi;
    visiblesize=2*texsize+1;

    % Create one single static grating image:
    x = meshgrid(-texsize:texsize + p, -texsize:texsize);
    grating = gray + inc*cos(fr*x);

    % Create circulaqr aperture for the alpha-channel:
    [x,y]=meshgrid(-texsize:texsize, -texsize:texsize);
    circle = white * (x.^2 + y.^2 <= (texsize)^2);

    % Set 2nd channel (the alpha channel) of 'grating' to the aperture
    % defined in 'circle':
    grating(:,:,2) = 0;
    grating(1:2*texsize+1, 1:2*texsize+1, 2) = circle;

    % Store alpha-masked grating in texture and attach the special 'glsl'
    % texture shader to it:
    gratingtex = Screen('MakeTexture', w, grating , [], [], [], [], glsl);
    
    % Definition of the drawn source rectangle on the screen:
    srcRect=[0 0 visiblesize visiblesize];

    % Query duration of monitor refresh interval:
    ifi=Screen('GetFlipInterval', w);

    waitframes = 1;
    waitduration = waitframes * ifi;

    % Recompute p, this time without the ceil() operation from above.
    % Otherwise we will get wrong drift speed due to rounding!
    p = 1/f; % pixels/cycle

    % Translate requested speed of the gratings (in cycles per second) into
    % a shift value in "pixels per frame", assuming given waitduration:
    shiftperframe = cyclespersecond * p * waitduration;
    
    % Perform initial Flip to sync us to the VBL and for getting an initial
    % VBL-Timestamp for our "WaitBlanking" emulation:
    vbl = Screen('Flip', w);
    
    % Run through all benchmark grid sizes
    for gridsize = 1:length(gridsizes)
    
        rotation_angles = linspace(1,360, gridsizes(gridsize));
        
%         % Compute size of each grating in the grid
%         sizeX = width;
%         sizeY = height;

        % We run at most 'blankDurationSecs' seconds.
        vblendtime = vbl + blankDurationSecs;

        % Blank loop: Run until timeout or keypress.
        while (vbl < vblendtime) && ~KbCheck
            % Flip 'waitframes' monitor refresh intervals after last redraw.
            vbl = Screen('Flip', w, vbl + (waitframes - 0.5) * ifi);
        end

        % We run at most 'movieDurationSecs' seconds.
        vblendtime = vbl + movieDurationSecs;
        i=0;

        colour = 0;
        % Animation loop: Run until timeout or keypress.
        while (vbl < vblendtime) && ~KbCheck

            % Shift the grating by "shiftperframe" pixels per frame. We pass
            % the pixel offset 'yoffset' as a parameter to
            % Screen('DrawTexture'). The attached 'glsl' texture draw shader
            % will apply this 'yoffset' pixel shift to the RGB or Luminance
            % color channels of the texture during drawing, thereby shifting
            % the gratings. Before drawing the shifted grating, it will mask it
            % with the "unshifted" alpha mask values inside the Alpha channel:
            yoffset = mod(i*shiftperframe,p);
            i=i+1;

            for k = 1:gridsizes(gridsize)
%               xoff = width/2;
%               yoff = height/2;
              srcRect=[0 0 visiblesize visiblesize];
              dstRect = [(width-height)/2 0 (width+height)/2 height];
%               disp(num2str(rotation_angles(k)));
              % Draw first grating texqtureq, rotated by "angle":
              global_alpha = 0.1;
              Screen('DrawTexture', w, gratingtex, srcRect, dstRect, rotation_angles(k), [], global_alpha, [], [], [], [0, yoffset, 0, 0]);
            end

            colour = 255 - colour;
            Screen('FillRect', w, colour, [0 height-200 200 height]);

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
    psychrethrow(psychlasterror);

end %try..catch..
