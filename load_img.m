function img = load_img(img_nos,file_def,det_type,roix,roiy,bg,read_par,norm,cosmic_remove)
%
% img = load_img(img_nos,file_def,'det_type'[,roix,roiy,bg,read_par,norm,cosmic_remove])
%
% Function to load images generated by MARCCD or GE detector.
%
% Input Parameters:
% img_nos: Image Numbers, specify the range or only a single picture.
% file_def: Structure consisting of file names.
% det_type: Detector type. 'marccd', marccd1k' and 'GE' are available.
% roix: The region of interest in X direction. Default is entire image.
% roiy: The region of interest in Y direction. Default is entire image.
% bg: If this is 1 global background subtraction will be performed.
%   If it is a 1x2 double local background subtraction will be performed
%   Default is 0 (nu subtraction).
% read_par: If different from 0 parameters from the parameter file will be 
%   added to the image structure.
% norm: if different from zero the images will be normalized by this number
%   divided by the diode value. Can only be done if read_par is also different from 0.
% cosmic_remove: If different from 0 cosmic rays will be removed from the
%   images.

% checking input parameters
if nargin < 3 
    error('Too few input parameters');
end
if nargin < 9
    cosmic_remove = 0;
end
if nargin < 8
    norm = 0;
end
if nargin < 7
    read_par = 0;
end
if nargin < 6
    bg = 0;
end
if nargin < 5
    roiy = [];
end
if nargin < 4
    roix = [];
end

% checking detector type
if ~(strcmp(det_type,'marccd') | strcmp(det_type,'marccd1k') | strcmp(det_type,'GE') | strcmp(det_type,'GE_NEW'))
    error('Wrong Detector Type. Only marccd, marccd1k and GE and GE_NEW are available.');    
end

% set the ROI if it is not specified
if isempty(roix) 
    if strcmp(det_type,'marccd') | strcmp(det_type,'GE') | strcmp(det_type,'GE_NEW')
        % High resolution: 2048 * 2048 images
        roix = 1:2048;
        roiy = 1:2048;
    elseif strcmp(det_type,'marccd1k') 
        % Low resolution: 1024 * 1024 images
        roix = 1:1024;
        roiy = 1:1024;
    end;
end;

% create empty image
img.im = zeros(length(roix),length(roiy),length(img_nos));

% bacgground image for GE detector
if strcmp(det_type,'GE') & ~isempty(file_def.GE.background) & bg ~= 0
    if exist([file_def.GE.imgpath file_def.GE.background])
        GE_bg = read_GE([file_def.GE.imgpath file_def.GE.background]);
        disp(['Loading background for GE ' file_def.GE.background ' ... done.']);
    else
        disp(['background for GE: "' file_def.GE.background '" not found.']);
    end
end

% bacgground image for GE_NEW detector
if strcmp(det_type,'GE_NEW') & ~isempty(file_def.GE.background) & bg ~= 0
    if exist([file_def.GE.imgpath file_def.GE.background])
        GE_bg = read_GE([file_def.GE.imgpath file_def.GE.background]);
        disp(['Loading background for GE ' file_def.GE.background ' ... done.']);
    else
        disp(['background for GE: "' file_def.GE.background '" not found.']);
    end
end


% starting the image structure
img.img_no = img_nos;
img.detector = det_type;
img.roix = roix;
img.roiy = roiy;
img.background_subtracted = 0;
if bg == 1
    img.background_subtracted_value = zeros(length(img_nos),4);
else
    img.background_subtracted_value = zeros(length(img_nos),1);    
end

% counting for the arrays in the image structure
ii = 1;
% reading images
for k = img_nos
    if k==-1 % insert an empty image
        img.filename{ii} = 'missing image';
        img.prefix{ii} = '';
    else
        % create the filling zeros for the filename
        if length(num2str(k)) < 6
            nn = '00000'; nn(length(nn)+1-length(num2str(k)):end)=num2str(k);
        else
            nn = num2str(k);
        end
        
        if strcmp(det_type,'marccd') 
            img.path = file_def.marccd.imgpath;        
            img.prefix{ii} = [file_def.marccd.prefix];
            img.filename{ii} = [file_def.marccd.prefix '_' nn '.tif'];
            % complete path
            path_image = [file_def.marccd.imgpath img.filename{ii}];    
            % checking if image exists
            if ~exist(path_image) & ~exist([path_image 'f'])
                disp(['Image: "' img.filename{ii} '" not found. Waiting for image. (Press Ctrl-C to abort)']);
            end
            % waits if it does not
            while ~exist(path_image) & ~exist([path_image 'f'])
                pause(1)
            end
            % reads image (checks for '.tif' or '.tiff')
            if exist(path_image)
                fullim = double(imread(path_image));
            else
                path_image = [path_image 'f'];
                img.filename{ii} = [img.filename{ii} 'f'];
                fullim = double(imread(path_image));
            end
            % background subtraction
            if length(bg)==1 & bg == 1
                [fullim background] = subtract_background_global(fullim,roix,roiy,15,100);
                img.im(:,:,ii) = fullim(roix,roiy);
                img.background_subtracted = 1;  
                img.background_subtracted_value(ii,:) = background;
            elseif length(bg)==1 & bg ~= 1
                img.im(:,:,ii) = fullim(roix,roiy) - bg;
                img.background_subtracted = 1;  
                img.background_subtracted_value(ii,:) = bg;                
            elseif length(bg)==2
                bgimage_up = fullim(roix(1)-bg(2):roix(1)-bg(1),roiy);
                bgimage_down = fullim(roix(end)+bg(1):roix(end)+bg(2),roiy);
                bg_mean = find_background_local(bgimage_up,[roix(1)-bg(2) roix(1)-bg(1)],bgimage_down,[roix(end)+bg(1) roix(end)+bg(2)],roix,100);
                img.im(:,:,ii) = fullim(roix,roiy);
                img.im(:,:,ii) = subtract_background_local(img.im(:,:,ii),bg_mean);
                img.background_subtracted = 1;  
                img.background_subtracted_value(ii) = bg_mean; 
                img.background_distribution_bins = [-30:30];
                img.background_distribution_values(ii,:) = histc([bgimage_up(:)' bgimage_down(:)']-bg_mean,img.background_distribution_bins);
            end
        elseif strcmp(det_type,'GE')
            img.path = file_def.GE.imgpath;
            img.prefix{ii} = [file_def.GE.prefix];
            img.filename{ii} = [file_def.GE.prefix '_' nn];
            % complete path
            path_image = [file_def.GE.imgpath img.filename{ii}];
            % checking if image exists        
            if ~exist(path_image)
                disp(['Image: "' img.filename{ii} '" not found. Waiting for image. (Press Ctrl-C to abort)']);
            end
            % waits if it does not
            while ~exist(path_image)
                pause(1)
            end
            % reads image
            fullim = read_GE(path_image);
            % background subtraction
            if ~isempty(file_def.GE.background) & bg ~= 0  
                fullim=fullim-GE_bg;
                img.background_subtracted = 1; 
                img.background=file_def.GE.background;
            end
            img.im(:,:,ii) =fullim(roix,roiy) ;        
        elseif strcmp(det_type,'GE_NEW')
            img.path = file_def.GE.imgpath;
            img.prefix{ii} = [file_def.GE.prefix];
            img.filename{ii} = [file_def.GE.prefix '_' nn];
            % complete path
            path_image = [file_def.GE.imgpath img.filename{ii}];
            % checking if image exists        
            if ~exist(path_image)
                disp(['Image: "' img.filename{ii} '" not found. Waiting for image. (Press Ctrl-C to abort)']);
            end
            % waits if it does not
            while ~exist(path_image)
                pause(1)
            end
            % reads image
            fullim = read_GE(path_image);
            % background subtraction
            if ~isempty(file_def.GE.background) & bg ~= 0  
                fullim=fullim-GE_bg;
                img.background_subtracted = 1; 
                img.background=file_def.GE.background;
            end
            img.im(:,:,ii) =fullim(roix,roiy) ;
        end
        disp([img.filename{ii} ' loaded.']);
    end
    % counting for the image structure    
    ii = ii + 1;
end

% read parameter file
if read_par ~= 0
    disp('reading parameters')
    img = find_img_par(img,file_def);
end

% normalizing with respect to diode value
img.normalized = 0;
if norm ~= 0 && read_par ~= 0
    disp('normalizing')
    img = normalize(img,norm);
end

% interpolate empty images
img = interpolate(img);

% removing cosmic rays 
img.cosmic_removed = 0;
if cosmic_remove ~= 0
    if length(img_nos)>1
        disp('removing cosmic rays')
        img = remove_cosmic_ray(img);
    end
end



