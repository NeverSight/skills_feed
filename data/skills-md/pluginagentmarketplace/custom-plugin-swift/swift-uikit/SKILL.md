---
name: swift-uikit
description: Master UIKit for iOS app development - views, view controllers, Auto Layout, table/collection views
version: "2.0.0"
sasmp_version: "1.3.0"
bonded_agent: 02-swift-ios
bond_type: PRIMARY_BOND
---

# UIKit Skill

Comprehensive UIKit framework knowledge for building traditional iOS user interfaces.

## Prerequisites

- Xcode 15+ installed
- iOS 15+ deployment target recommended
- Understanding of MVC/MVVM patterns

## Parameters

```yaml
parameters:
  layout_approach:
    type: string
    enum: [programmatic, storyboard, xib]
    default: programmatic
  accessibility_enabled:
    type: boolean
    default: true
  dynamic_type_support:
    type: boolean
    default: true
```

## Topics Covered

### View Controllers
| Type | Purpose | Use Case |
|------|---------|----------|
| `UIViewController` | Base controller | Custom screens |
| `UINavigationController` | Stack navigation | Hierarchical flow |
| `UITabBarController` | Tab-based | Main sections |
| `UISplitViewController` | Master-detail | iPad layouts |
| `UIPageViewController` | Page swiping | Onboarding |

### Auto Layout
| Constraint Type | Description |
|-----------------|-------------|
| Leading/Trailing | Horizontal edges (respects RTL) |
| Top/Bottom | Vertical edges |
| CenterX/CenterY | Center alignment |
| Width/Height | Size constraints |
| Aspect Ratio | Proportional sizing |

### Table & Collection Views
| Component | Purpose |
|-----------|---------|
| UITableView | Vertical scrolling lists |
| UICollectionView | Flexible grid layouts |
| DiffableDataSource | Automatic diffing (iOS 13+) |
| CompositionalLayout | Complex layouts (iOS 13+) |

## Code Examples

### Programmatic View Controller
```swift
final class ProfileViewController: UIViewController {
    // MARK: - UI Components

    private lazy var avatarImageView: UIImageView = {
        let imageView = UIImageView()
        imageView.contentMode = .scaleAspectFill
        imageView.clipsToBounds = true
        imageView.layer.cornerRadius = 50
        imageView.translatesAutoresizingMaskIntoConstraints = false
        imageView.accessibilityLabel = "Profile picture"
        return imageView
    }()

    private lazy var nameLabel: UILabel = {
        let label = UILabel()
        label.font = .preferredFont(forTextStyle: .title1)
        label.adjustsFontForContentSizeCategory = true
        label.textAlignment = .center
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()

    private lazy var bioLabel: UILabel = {
        let label = UILabel()
        label.font = .preferredFont(forTextStyle: .body)
        label.adjustsFontForContentSizeCategory = true
        label.numberOfLines = 0
        label.textAlignment = .center
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()

    // MARK: - Lifecycle

    override func viewDidLoad() {
        super.viewDidLoad()
        setupUI()
        setupConstraints()
    }

    // MARK: - Setup

    private func setupUI() {
        view.backgroundColor = .systemBackground
        view.addSubview(avatarImageView)
        view.addSubview(nameLabel)
        view.addSubview(bioLabel)
    }

    private func setupConstraints() {
        NSLayoutConstraint.activate([
            avatarImageView.topAnchor.constraint(equalTo: view.safeAreaLayoutGuide.topAnchor, constant: 32),
            avatarImageView.centerXAnchor.constraint(equalTo: view.centerXAnchor),
            avatarImageView.widthAnchor.constraint(equalToConstant: 100),
            avatarImageView.heightAnchor.constraint(equalToConstant: 100),

            nameLabel.topAnchor.constraint(equalTo: avatarImageView.bottomAnchor, constant: 16),
            nameLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            nameLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20),

            bioLabel.topAnchor.constraint(equalTo: nameLabel.bottomAnchor, constant: 8),
            bioLabel.leadingAnchor.constraint(equalTo: view.leadingAnchor, constant: 20),
            bioLabel.trailingAnchor.constraint(equalTo: view.trailingAnchor, constant: -20)
        ])
    }

    // MARK: - Configuration

    func configure(with user: User) {
        nameLabel.text = user.name
        bioLabel.text = user.bio
        // Load avatar image
    }
}
```

### Modern Collection View with Diffable Data Source
```swift
final class ProductGridViewController: UIViewController {
    enum Section { case main }

    private var collectionView: UICollectionView!
    private var dataSource: UICollectionViewDiffableDataSource<Section, Product>!

    override func viewDidLoad() {
        super.viewDidLoad()
        configureCollectionView()
        configureDataSource()
    }

    private func configureCollectionView() {
        let layout = createCompositionalLayout()
        collectionView = UICollectionView(frame: view.bounds, collectionViewLayout: layout)
        collectionView.autoresizingMask = [.flexibleWidth, .flexibleHeight]
        collectionView.backgroundColor = .systemBackground
        view.addSubview(collectionView)
    }

    private func createCompositionalLayout() -> UICollectionViewLayout {
        let itemSize = NSCollectionLayoutSize(
            widthDimension: .fractionalWidth(0.5),
            heightDimension: .estimated(200)
        )
        let item = NSCollectionLayoutItem(layoutSize: itemSize)
        item.contentInsets = NSDirectionalEdgeInsets(top: 8, leading: 8, bottom: 8, trailing: 8)

        let groupSize = NSCollectionLayoutSize(
            widthDimension: .fractionalWidth(1.0),
            heightDimension: .estimated(200)
        )
        let group = NSCollectionLayoutGroup.horizontal(layoutSize: groupSize, subitems: [item])

        let section = NSCollectionLayoutSection(group: group)
        return UICollectionViewCompositionalLayout(section: section)
    }

    private func configureDataSource() {
        let cellRegistration = UICollectionView.CellRegistration<ProductCell, Product> { cell, indexPath, product in
            cell.configure(with: product)
        }

        dataSource = UICollectionViewDiffableDataSource<Section, Product>(collectionView: collectionView) {
            collectionView, indexPath, product in
            collectionView.dequeueConfiguredReusableCell(using: cellRegistration, for: indexPath, item: product)
        }
    }

    func applySnapshot(products: [Product], animatingDifferences: Bool = true) {
        var snapshot = NSDiffableDataSourceSnapshot<Section, Product>()
        snapshot.appendSections([.main])
        snapshot.appendItems(products)
        dataSource.apply(snapshot, animatingDifferences: animatingDifferences)
    }
}
```

### Custom UIView with Intrinsic Size
```swift
final class TagView: UIView {
    private let label: UILabel = {
        let label = UILabel()
        label.font = .preferredFont(forTextStyle: .caption1)
        label.adjustsFontForContentSizeCategory = true
        label.translatesAutoresizingMaskIntoConstraints = false
        return label
    }()

    private let padding = UIEdgeInsets(top: 4, left: 8, bottom: 4, right: 8)

    override var intrinsicContentSize: CGSize {
        let labelSize = label.intrinsicContentSize
        return CGSize(
            width: labelSize.width + padding.left + padding.right,
            height: labelSize.height + padding.top + padding.bottom
        )
    }

    override init(frame: CGRect) {
        super.init(frame: frame)
        setup()
    }

    required init?(coder: NSCoder) {
        super.init(coder: coder)
        setup()
    }

    private func setup() {
        backgroundColor = .systemBlue
        layer.cornerRadius = 8

        addSubview(label)
        NSLayoutConstraint.activate([
            label.topAnchor.constraint(equalTo: topAnchor, constant: padding.top),
            label.leadingAnchor.constraint(equalTo: leadingAnchor, constant: padding.left),
            label.trailingAnchor.constraint(equalTo: trailingAnchor, constant: -padding.right),
            label.bottomAnchor.constraint(equalTo: bottomAnchor, constant: -padding.bottom)
        ])
    }

    func configure(text: String, color: UIColor = .systemBlue) {
        label.text = text
        label.textColor = .white
        backgroundColor = color
        invalidateIntrinsicContentSize()
    }
}
```

## Troubleshooting

### Common Issues

| Issue | Cause | Solution |
|-------|-------|----------|
| "Unable to simultaneously satisfy constraints" | Conflicting constraints | Lower priority on flexible constraints |
| Cell not appearing | Missing registration | Use CellRegistration or register before dequeue |
| Keyboard covers text field | No keyboard handling | Observe keyboard notifications |
| Content compressed | Missing hugging priority | Set content hugging priority higher |
| View not responding to touches | Overlapping views | Check view hierarchy, userInteractionEnabled |

### Debug Commands
```swift
// Print view hierarchy
po view.recursiveDescription()

// Print Auto Layout issues
po view.constraintsAffectingLayout(for: .horizontal)

// Check if on main thread
assert(Thread.isMainThread, "UI updates must be on main thread")
```

## Validation Rules

```yaml
validation:
  - rule: accessibility_labels
    severity: warning
    check: All interactive elements must have accessibility labels
  - rule: dynamic_type_support
    severity: warning
    check: Use preferredFont and adjustsFontForContentSizeCategory
  - rule: safe_area_constraints
    severity: info
    check: Content should respect safe area layout guides
```

## Usage

```
Skill("swift-uikit")
```

## Related Skills

- `swift-ios-basics` - iOS fundamentals
- `swift-swiftui` - Modern alternative
- `swift-architecture` - App architecture
