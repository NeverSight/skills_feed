---
name: algorithmic-art
description: Generate creative coding art using Canvas, SVG, WebGL, and generative algorithms. Use when creating algorithmic art or generative designs.
---

# Algorithmic Art Skill

p5.jsを使ったジェネラティブアートを生成するスキルです。

## 概要

アルゴリズムとランダム性を組み合わせて、ユニークな視覚芸術を創造します。

## 主な機能

- **生成的デザイン**: パターン、フラクタル、パーティクル
- **シード値**: 再現可能なランダムアート
- **アニメーション**: 動的な視覚効果
- **インタラクティブ**: マウス・キーボード入力
- **エクスポート**: PNG、SVG、GIF

## 使用方法

```
p5.jsで以下のアートを生成：
- タイプ: パーティクルシステム
- 色: 青系グラデーション
- アニメーション: あり
```

## 生成例

### フローフィールド

```javascript
let particles = [];
let flowfield;
let cols, rows;
let scale = 20;

function setup() {
  createCanvas(800, 600);
  cols = floor(width / scale);
  rows = floor(height / scale);
  flowfield = new Array(cols * rows);

  for (let i = 0; i < 1000; i++) {
    particles[i] = new Particle();
  }

  background(255);
}

function draw() {
  let yoff = 0;
  for (let y = 0; y < rows; y++) {
    let xoff = 0;
    for (let x = 0; x < cols; x++) {
      let index = x + y * cols;
      let angle = noise(xoff, yoff, frameCount * 0.001) * TWO_PI * 4;
      let v = p5.Vector.fromAngle(angle);
      v.setMag(1);
      flowfield[index] = v;
      xoff += 0.1;
    }
    yoff += 0.1;
  }

  for (let particle of particles) {
    particle.follow(flowfield);
    particle.update();
    particle.edges();
    particle.show();
  }
}

class Particle {
  constructor() {
    this.pos = createVector(random(width), random(height));
    this.vel = createVector(0, 0);
    this.acc = createVector(0, 0);
    this.maxspeed = 4;
  }

  follow(vectors) {
    let x = floor(this.pos.x / scale);
    let y = floor(this.pos.y / scale);
    let index = x + y * cols;
    let force = vectors[index];
    this.applyForce(force);
  }

  applyForce(force) {
    this.acc.add(force);
  }

  update() {
    this.vel.add(this.acc);
    this.vel.limit(this.maxspeed);
    this.pos.add(this.vel);
    this.acc.mult(0);
  }

  show() {
    stroke(0, 5);
    strokeWeight(1);
    point(this.pos.x, this.pos.y);
  }

  edges() {
    if (this.pos.x > width) this.pos.x = 0;
    if (this.pos.x < 0) this.pos.x = width;
    if (this.pos.y > height) this.pos.y = 0;
    if (this.pos.y < 0) this.pos.y = height;
  }
}
```

### 再帰的なフラクタルツリー

```javascript
function setup() {
  createCanvas(800, 800);
  background(255);
}

function draw() {
  background(255);
  translate(width / 2, height);
  stroke(0);
  branch(100);
}

function branch(len) {
  line(0, 0, 0, -len);
  translate(0, -len);

  if (len > 4) {
    push();
    rotate(PI / 4);
    branch(len * 0.67);
    pop();

    push();
    rotate(-PI / 4);
    branch(len * 0.67);
    pop();
  }
}
```

## アートスタイル

- **フローフィールド**: パーリンノイズベースの流線
- **フラクタル**: 再帰的なパターン
- **パーティクルシステム**: 動的な粒子
- **幾何学パターン**: 規則的な図形
- **オーガニック**: 自然を模倣

## バージョン情報

- スキルバージョン: 1.0.0
- 最終更新: 2025-01-22
