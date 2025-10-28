import * as THREE from 'three';
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';
import { OrbitControls } from 'three/addons/controls/OrbitControls.js';

let scene, camera, renderer, controls;
let tvScreenMesh;
let directionalLight, pointLight; // Main lights to be toggled
let isLightOn = true;

// --- Game Variables ---
const game = {
	canvas: null,
	context: null,
	texture: null,
	player: {
		x: 50,
		y: 300,
		width: 20,
		height: 20,
		vx: 0, // Velocity X
		vy: 0, // Velocity Y
		isJumping: true,
	},
	keys: {
		ArrowLeft: false,
		ArrowRight: false,
		Space: false,
	},
	gravity: 0.4,
	friction: 0.8, // Slows down the player
	jumpStrength: 10,
	moveSpeed: 3,
	platforms: [
        // The main floor
		{ x: 0, y: 380, width: 400, height: 20 },
        // Some platforms
		{ x: 100, y: 320, width: 80, height: 10 },
		{ x: 220, y: 260, width: 80, height: 10 },
		{ x: 50, y: 200, width: 80, height: 10 },
        { x: 300, y: 200, width: 30, height: 80 }, // A wall
	],
};

// --- Core Functions ---

function init() {
	// Create the 3D scene
	scene = new THREE.Scene();
	scene.background = new THREE.Color(0x111111);

	// Create a renderer and add it to the DOM
	renderer = new THREE.WebGLRenderer({ antialias: true });
	renderer.setSize(window.innerWidth, window.innerHeight);
	document.body.appendChild(renderer.domElement);

	// --- Camera ---
	const aspect = window.innerWidth / window.innerHeight;
	const frustumSize = 5;
	camera = new THREE.OrthographicCamera(
		frustumSize * aspect / -2,
		frustumSize * aspect / 2,
		frustumSize / 2,
		frustumSize / -2,
		0.1,
		100
	);
	camera.position.set(5, 5, 5);
	camera.lookAt(scene.position);
	scene.add(camera);

	// --- Controls ---
	controls = new OrbitControls(camera, renderer.domElement);
	controls.enableZoom = true;
	controls.enablePan = false;
	controls.target.set(0, 1.5, 0);
	controls.update();

	// --- Lights ---
    // 1. Base Ambient Light (Always On)
	const baseAmbientLight = new THREE.AmbientLight(0xffffff, 0.2);
	scene.add(baseAmbientLight);

    // 2. Main Directional Light (Toggled)
	directionalLight = new THREE.DirectionalLight(0xffffff, 1.0); // Reduced intensity
	directionalLight.position.set(10, 10, 5);
	scene.add(directionalLight);
    
    // 3. Professional Point Light (Toggled)
    pointLight = new THREE.PointLight(0xffffff, 0.8, 10); // color, intensity, distance
    pointLight.position.set(0, 3.5, 0); // Positioned high in the room
    scene.add(pointLight);


	// --- Load Model ---
	loadModel();

	// --- Setup Game ---
	initPlatformerGame();

	// --- Input Listeners ---
	window.addEventListener('keydown', handleGameInput);
	window.addEventListener('keyup', handleGameInput);
	document.getElementById('info').innerText = 'Use Arrow Keys & Space. Press L to toggle lights.';

	// Handle window resizing
	window.addEventListener('resize', onWindowResize);

	// Start the render loop
	animate();
}

function loadModel() {
	const loader = new GLTFLoader();
	loader.load(
		'Room.glb',
		function (gltf) {
			const model = gltf.scene;
			model.traverse((child) => {
				if (child.isMesh && child.name === 'TV_SCREEN') {
					tvScreenMesh = child;
					console.log('Found TV Screen Mesh:', tvScreenMesh);
				}
			});
			scene.add(model);
		},
		undefined,
		function (error) {
			console.error('An error happened while loading the model:', error);
			document.getElementById('info').innerText = 'Error: Could not load Room.glb model.';
		}
	);
}

// --- Platformer Game Logic ---

function initPlatformerGame() {
	// 1. Create an off-screen canvas
	game.canvas = document.createElement('canvas');
	game.canvas.width = 400; // Game resolution
	game.canvas.height = 400;
	game.context = game.canvas.getContext('2d');

	// 2. Create a texture from this canvas
	game.texture = new THREE.CanvasTexture(game.canvas);
	game.texture.flipY = false;
	game.texture.encoding = THREE.sRGBEncoding;

	// 3. Create a material from the texture
	const screenMaterial = new THREE.MeshBasicMaterial({
		map: game.texture,
	});

	// 4. Apply the material to the TV screen
	const checkMeshInterval = setInterval(() => {
		if (tvScreenMesh) {
			clearInterval(checkMeshInterval);
			tvScreenMesh.material = screenMaterial;
		}
	}, 100);
}

function handleGameInput(e) {
	// Prevent keys from scrolling the page
	if (["ArrowUp", "ArrowDown", "ArrowLeft", "ArrowRight", " ", "l", "L"].includes(e.key)) {
		e.preventDefault();
	}

	const isKeyDown = e.type === 'keydown';

    // --- Light Toggle Logic ---
    if ((e.key === 'l' || e.key === 'L') && isKeyDown) {
        isLightOn = !isLightOn; // Flip the state
        // Only toggle the main lights
        directionalLight.visible = isLightOn;
        pointLight.visible = isLightOn;
    }

    // --- Game Input Logic ---
	if (e.key === 'ArrowLeft') game.keys.ArrowLeft = isKeyDown;
	if (e.key === 'ArrowRight') game.keys.ArrowRight = isKeyDown;
	if (e.key === ' ') game.keys.Space = isKeyDown; // Spacebar for jump
}

function resetGame() {
	game.player.x = 50;
	game.player.y = 300;
	game.player.vx = 0;
	game.player.vy = 0;
	game.player.isJumping = true;
}

function gameLoop() {
	// --- 1. Handle Input ---
	if (game.keys.ArrowLeft) {
		game.player.vx = -game.moveSpeed;
	} else if (game.keys.ArrowRight) {
		game.player.vx = game.moveSpeed;
	} else {
		game.player.vx *= game.friction; // Apply friction when no key is pressed
	}

	if (game.keys.Space && !game.player.isJMumping) {
		game.player.vy = -game.jumpStrength;
		game.player.isJumping = true;
	}

	// --- 2. Apply Physics ---
	game.player.vy += game.gravity; // Apply gravity
	game.player.x += game.player.vx;
	game.player.y += game.player.vy;

	let onPlatform = false;

	// --- 3. Handle Collisions ---
	for (const p of game.platforms) {
		// Check for AABB (Axis-Aligned Bounding Box) collision
		if (
			game.player.x < p.x + p.width &&
			game.player.x + game.player.width > p.x &&
			game.player.y < p.y + p.height &&
			game.player.y + game.player.height > p.y
		) {
			// Check if the player was *above* the platform in the previous frame
            // This ensures we only collide with the top
			const prevPlayerBottom = (game.player.y - game.player.vy) + game.player.height;
            
			if (game.player.vy > 0 && prevPlayerBottom <= p.y) {
				// Player is landing on top
				game.player.y = p.y - game.player.height; // Snap to platform top
				game.player.vy = 0;
				game.player.isJumping = false;
				onPlatform = true;
			} else if (game.player.vy < 0 && game.player.y < p.y + p.height && (game.player.y - game.player.vy) > p.y + p.height) {
                // Player is hitting bottom of platform
                game.player.y = p.y + p.height;
                game.player.vy = 0;
            } else if (game.player.vx > 0 && (game.player.x - game.player.vx) + game.player.width <= p.x) {
                // Player is hitting left side of platform
                game.player.x = p.x - game.player.width;
                game.player.vx = 0;
            } else if (game.player.vx < 0 && (game.player.x - game.player.vx) >= p.x + p.width) {
                // Player is hitting right side of platform
                game.player.x = p.x + p.width;
                game.player.vx = 0;
            }
		}
	}
    
    // If we are in the air (not on a platform), we are jumping
    if (!onPlatform) {
        game.player.isJumping = true;
    }

	// --- 4. Handle Screen Boundaries ---
	// Stop at left/right edges
	if (game.player.x < 0) {
        game.player.x = 0;
        game.player.vx = 0;
    }
	if (game.player.x + game.player.width > game.canvas.width) {
		game.player.x = game.canvas.width - game.player.width;
        game.player.vx = 0;
	}

	// Check if player fell off the bottom
	if (game.player.y > game.canvas.height) {
		resetGame();
	}

	// --- 5. Draw Game ---
	const ctx = game.context;

	// Draw Sky
	ctx.fillStyle = '#4a90e2'; // Sky blue
	ctx.fillRect(0, 0, game.canvas.width, game.canvas.height);

	// Draw Platforms
	ctx.fillStyle = '#4caf50'; // Green
	for (const p of game.platforms) {
		ctx.fillRect(p.x, p.y, p.width, p.height);
	}

	// Draw Player
	ctx.fillStyle = '#e53935'; // Red "Mario"
	ctx.fillRect(game.player.x, game.player.y, game.player.width, game.player.height);

	// --- 6. Update 3D Texture ---
	if (game.texture) {
		game.texture.needsUpdate = true;
	}
}

// --- Helper Functions ---

function onWindowResize() {
	const aspect = window.innerWidth / window.innerHeight;
	const frustumSize = 5;

	camera.left = frustumSize * aspect / -2;
	camera.right = frustumSize * aspect / 2;
	camera.top = frustumSize / 2;
	camera.bottom = frustumSize / -2;

	camera.updateProjectionMatrix();
	renderer.setSize(window.innerWidth, window.innerHeight);
}

function animate() {
	requestAnimationFrame(animate);

	// Call the game loop
	gameLoop();

	controls.update(); // Update controls
	renderer.render(scene, camera); // Render the 3D scene
}

// --- Start ---
init();