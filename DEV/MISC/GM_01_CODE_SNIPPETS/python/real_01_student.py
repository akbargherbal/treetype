#!/usr/bin/env python3
"""
student.py - Student Model CLI Tool
Tracks conceptual knowledge mastery across learning sessions.
Phase 1, 2, and 3 Complete (including batch operations)
"""

import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional

# Default data file location
DATA_FILE = Path.home() / "student_model.json"

# JSON Schema for student model
SCHEMA_VERSION = "1.0"

def get_default_model() -> Dict[str, Any]:
    """Return the default/empty student model structure."""
    return {
        "schema_version": SCHEMA_VERSION,
        "metadata": {
            "created": datetime.now().isoformat(),
            "last_updated": datetime.now().isoformat(),
            "student_profile": ""
        },
        "concepts": {},
        "misconceptions": [],
        "sessions": []
    }

def validate_model(model: Dict[str, Any]) -> bool:
    """Validate that model has required structure."""
    required_keys = ["metadata", "concepts", "sessions"]
    if not all(key in model for key in required_keys):
        return False

    required_metadata = ["created", "last_updated"]
    if not all(key in model["metadata"] for key in required_metadata):
        return False

    return True

def load_model() -> Dict[str, Any]:
    """
    Load the student model from disk with error handling.
    Creates a new model if file doesn't exist.
    """
    if not DATA_FILE.exists():
        print(f"ℹ️  No model found at {DATA_FILE}")
        print("   Run 'python student.py init' to create one")
        return get_default_model()

    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            model = json.load(f)

        # Validate structure
        if not validate_model(model):
            print(f"⚠️  Model at {DATA_FILE} has invalid structure")

            # Check for backup
            backup = DATA_FILE.with_suffix('.json.backup')
            if backup.exists():
                print(f"   Attempting to restore from backup...")
                with open(backup, 'r', encoding='utf-8') as f:
                    model = json.load(f)
                if validate_model(model):
                    print("✅ Restored from backup successfully")
                    save_model(model)  # Save the good backup as main file
                    return model

            print("   Creating new model")
            return get_default_model()

        return model

    except json.JSONDecodeError as e:
        print(f"❌ Error: Corrupt JSON in {DATA_FILE}")
        print(f"   {str(e)}")

        # Try backup
        backup = DATA_FILE.with_suffix('.json.backup')
        if backup.exists():
            print(f"   Attempting to restore from backup...")
            try:
                with open(backup, 'r', encoding='utf-8') as f:
                    model = json.load(f)
                if validate_model(model):
                    print("✅ Restored from backup successfully")
                    save_model(model)
                    return model
            except:
                pass

        print("   Creating new model")
        return get_default_model()

    except Exception as e:
        print(f"❌ Unexpected error loading model: {str(e)}")
        return get_default_model()


def save_model(model: Dict[str, Any]) -> bool:
    """
    Save model to disk with atomic writes and backup.
    Returns True on success, False on failure.
    """
    try:
        # Validate before saving
        if not validate_model(model):
            print("❌ Error: Model structure is invalid, refusing to save")
            return False

        # Update timestamp
        model["metadata"]["last_updated"] = datetime.now().isoformat()

        # Backup existing file (before any write operations)
        if DATA_FILE.exists():
            backup = DATA_FILE.with_suffix('.json.backup')
            shutil.copy(DATA_FILE, backup)

        # Write to temp file first (atomic operation)
        temp = DATA_FILE.with_suffix('.json.tmp')
        with open(temp, 'w', encoding='utf-8') as f:
            json.dump(model, f, indent=2, ensure_ascii=False)

        # Atomic rename
        temp.replace(DATA_FILE)

        # Create backup after successful save (if it doesn't exist yet)
        backup = DATA_FILE.with_suffix('.json.backup')
        if not backup.exists():
            shutil.copy(DATA_FILE, backup)

        return True

    except Exception as e:
        print(f"❌ Error saving model: {str(e)}")
        return False

def initialize_model(profile: str = "") -> Dict[str, Any]:
    """
    Create a new student model and save it to disk.
    """
    if DATA_FILE.exists():
        response = input(f"⚠️  Model already exists at {DATA_FILE}. Overwrite? (yes/no): ")
        if response.lower() not in ['yes', 'y']:
            print("Cancelled.")
            return load_model()

    model = get_default_model()
    if profile:
        model["metadata"]["student_profile"] = profile

    if save_model(model):
        print(f"✅ Initialized new student model at {DATA_FILE}")
        print(f"   Created: {model['metadata']['created']}")
        if profile:
            print(f"   Profile: {profile}")
    else:
        print("❌ Failed to initialize model")

    return model

def find_concept(model: Dict[str, Any], concept_name: str) -> Optional[str]:
    """
    Find a concept by name (case-insensitive).
    Returns the exact key from the model, or None if not found.
    """
    concept_lower = concept_name.lower()
    for key in model["concepts"].keys():
        if key.lower() == concept_lower:
            return key
    return None


# =============================================================================
# CLI COMMAND HANDLERS
# =============================================================================

# PHASE 1: Core commands

def cmd_init(args):
    """Initialize a new student model."""
    initialize_model(args.profile if hasattr(args, 'profile') else "")

def cmd_info(args):
    """Show model metadata and statistics."""
    model = load_model()

    print("📊 Student Model Information")
    print(f"   Location:      {DATA_FILE}")
    print(f"   Created:       {model['metadata']['created'].split('T')[0]}")
    print(f"   Last Updated:  {model['metadata']['last_updated'].split('T')[0]}")

    if model['metadata'].get('student_profile'):
        print(f"   Profile:       {model['metadata']['student_profile']}")

    print(f"\n   Total Concepts: {len(model['concepts'])}")
    print(f"   Total Sessions: {len(model['sessions'])}")

    if model['concepts']:
        masteries = [c.get('mastery', 0) for c in model['concepts'].values()]
        avg_mastery = sum(masteries) / len(masteries)
        print(f"   Avg Mastery:    {avg_mastery:.1f}%")


# PHASE 2: Read operations

def cmd_list(args):
    """List all concepts with summary info."""
    model = load_model()

    if not model['concepts']:
        print("📚 No concepts tracked yet.")
        print("   Add your first concept with: python student.py add \"Concept Name\" 50 medium")
        return

    print(f"📚 Tracked Concepts ({len(model['concepts'])} total)\n")

    # Sort by mastery (descending) for better overview
    sorted_concepts = sorted(
        model['concepts'].items(),
        key=lambda x: x[1].get('mastery', 0),
        reverse=True
    )

    for name, data in sorted_concepts:
        mastery = data.get('mastery', 0)
        confidence = data.get('confidence', 'unknown')
        last_reviewed = data.get('last_reviewed', 'never')

        # Format last reviewed date
        if last_reviewed != 'never':
            last_reviewed = last_reviewed.split('T')[0]

        # Mastery indicator
        if mastery >= 80:
            indicator = "✅"
        elif mastery >= 60:
            indicator = "🟡"
        elif mastery >= 40:
            indicator = "🟠"
        else:
            indicator = "🔴"

        # Confidence indicator
        conf_display = confidence
        if confidence == "low":
            conf_display = "⚠️  low"

        print(f"{indicator} {name:<40} {mastery:>3}%  {conf_display:<12} (last: {last_reviewed})")

    print(f"\nLegend: ✅ 80%+  🟡 60-79%  🟠 40-59%  🔴 <40%")


def cmd_show(args):
    """Show detailed information about a specific concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        print(f"   Run 'python student.py list' to see tracked concepts.")
        return

    concept = model['concepts'][concept_key]

    print(f"📊 Concept: {concept_key}")
    print(f"   Mastery:          {concept.get('mastery', 'N/A')}%")
    print(f"   Confidence:       {concept.get('confidence', 'N/A')}")

    # Dates
    first = concept.get('first_encountered', 'N/A')
    last = concept.get('last_reviewed', 'N/A')
    if first != 'N/A':
        first = first.split('T')[0]
    if last != 'N/A':
        last = last.split('T')[0]

    print(f"   First Encountered: {first}")
    print(f"   Last Reviewed:     {last}")

    # Struggles
    struggles = concept.get('struggles', [])
    if struggles:
        print(f"   ⚠️  Struggles:")
        for struggle in struggles:
            print(f"      - {struggle}")

    # Breakthroughs
    breakthroughs = concept.get('breakthroughs', [])
    if breakthroughs:
        print(f"   💡 Breakthroughs:")
        for breakthrough in breakthroughs:
            print(f"      - {breakthrough}")

    # Related concepts
    related = concept.get('related_concepts', [])
    if related:
        print(f"   🔗 Related Concepts:")
        for rel_name in related:
            rel_key = find_concept(model, rel_name)
            if rel_key and rel_key in model['concepts']:
                rel_data = model['concepts'][rel_key]
                rel_mastery = rel_data.get('mastery', 0)
                rel_last = rel_data.get('last_reviewed', 'never')
                if rel_last != 'never':
                    rel_last = rel_last.split('T')[0]

                # Flag low mastery prerequisites
                if rel_mastery < 60:
                    print(f"      - {rel_name} (Mastery: {rel_mastery}%, Last: {rel_last}) ⚠️ LOW")
                else:
                    print(f"      - {rel_name} (Mastery: {rel_mastery}%, Last: {rel_last}) ✓")
            else:
                print(f"      - {rel_name} (not tracked)")


def cmd_related(args):
    """Show concepts related to a specific concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    concept = model['concepts'][concept_key]
    related = concept.get('related_concepts', [])

    if not related:
        print(f"🔗 No related concepts tracked for '{concept_key}'")
        print(f"   Link concepts with: python student.py link \"{concept_key}\" \"Related Concept\"")
        return

    print(f"🔗 Concepts related to '{concept_key}':")

    for rel_name in related:
        rel_key = find_concept(model, rel_name)
        if rel_key and rel_key in model['concepts']:
            rel_data = model['concepts'][rel_key]
            rel_mastery = rel_data.get('mastery', 0)
            rel_confidence = rel_data.get('confidence', 'unknown')
            rel_last = rel_data.get('last_reviewed', 'never')

            if rel_last != 'never':
                rel_last = rel_last.split('T')[0]

            # Status indicator
            if rel_mastery < 60:
                status = "⚠️ LOW"
            else:
                status = "✓"

            print(f"   - {rel_name:<40} {rel_mastery:>3}%  {rel_confidence:<10}  (last: {rel_last}) {status}")
        else:
            print(f"   - {rel_name} (not tracked yet)")


# PHASE 3: Write operations

def cmd_add(args):
    """Add a new concept."""
    model = load_model()

    # Check for existing concept
    if find_concept(model, args.concept_name):
        print(f"❌ Concept '{args.concept_name}' already exists.")
        print(f"   Use 'python student.py update' to modify it.")
        return

    # Validate mastery range
    if not (0 <= args.mastery <= 100):
        print(f"❌ Mastery must be 0-100, got {args.mastery}")
        return

    # Validate confidence (argparse choices handles this, but be explicit)
    if args.confidence not in ['low', 'medium', 'high']:
        print(f"❌ Confidence must be: low, medium, or high")
        return

    # Create new concept
    model["concepts"][args.concept_name] = {
        "mastery": args.mastery,
        "confidence": args.confidence,
        "first_encountered": datetime.now().isoformat(),
        "last_reviewed": datetime.now().isoformat(),
        "struggles": [],
        "breakthroughs": [],
        "related_concepts": []
    }

    # Handle related concepts if provided
    if hasattr(args, 'related') and args.related:
        related_list = [r.strip() for r in args.related.split(',')]
        model["concepts"][args.concept_name]["related_concepts"] = related_list

        # Warn about untracked related concepts
        for rel in related_list:
            if not find_concept(model, rel):
                print(f"⚠️  Related concept '{rel}' not tracked yet.")

    if save_model(model):
        print(f"✅ Added concept: '{args.concept_name}'")
        print(f"   Mastery: {args.mastery}%")
        print(f"   Confidence: {args.confidence}")
        if hasattr(args, 'related') and args.related:
            print(f"   Related: {args.related}")
    else:
        print("❌ Failed to save model")


def cmd_update(args):
    """Update an existing concept's mastery and/or confidence."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        print(f"   Run 'python student.py list' to see tracked concepts.")
        return

    concept = model["concepts"][concept_key]
    updated = []

    # Update mastery if provided
    if args.mastery is not None:
        if not (0 <= args.mastery <= 100):
            print(f"❌ Mastery must be 0-100, got {args.mastery}")
            return

        old = concept.get('mastery', 0)
        concept['mastery'] = args.mastery
        updated.append(f"mastery {old}% → {args.mastery}%")

    # Update confidence if provided
    if args.confidence is not None:
        if args.confidence not in ['low', 'medium', 'high']:
            print(f"❌ Confidence must be: low, medium, or high")
            return

        old = concept.get('confidence', 'unknown')
        concept['confidence'] = args.confidence
        updated.append(f"confidence {old} → {args.confidence}")

    # Always update last_reviewed timestamp
    concept['last_reviewed'] = datetime.now().isoformat()

    if updated:
        if save_model(model):
            print(f"✅ Updated '{concept_key}':")
            for change in updated:
                print(f"   {change}")
        else:
            print("❌ Failed to save model")
    else:
        print("ℹ️  No changes specified")
        print("   Use --mastery N or --confidence [low|medium|high]")


def cmd_struggle(args):
    """Log a struggle with a concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        print(f"   Add it first: python student.py add \"{args.concept_name}\" 0 low")
        return

    concept = model["concepts"][concept_key]

    # Check for duplicate struggles
    struggles = concept.get('struggles', [])
    if args.description in struggles:
        print(f"ℹ️  This struggle already logged.")
        return

    # Add the struggle
    concept.setdefault('struggles', []).append(args.description)
    concept['last_reviewed'] = datetime.now().isoformat()

    if save_model(model):
        print(f"✅ Logged struggle for '{concept_key}'")
        print(f"   \"{args.description}\"")
    else:
        print("❌ Failed to save model")


def cmd_breakthrough(args):
    """Log a breakthrough with a concept."""
    model = load_model()
    concept_key = find_concept(model, args.concept_name)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        print(f"   Add it first: python student.py add \"{args.concept_name}\" 0 low")
        return

    concept = model["concepts"][concept_key]

    # Check for duplicate breakthroughs
    breakthroughs = concept.get('breakthroughs', [])
    if args.description in breakthroughs:
        print(f"ℹ️  This breakthrough already logged.")
        return

    # Add the breakthrough
    concept.setdefault('breakthroughs', []).append(args.description)
    concept['last_reviewed'] = datetime.now().isoformat()

    if save_model(model):
        print(f"✅ Logged breakthrough for '{concept_key}'")
        print(f"   💡 \"{args.description}\"")
    else:
        print("❌ Failed to save model")


def cmd_link(args):
    """Link two concepts (create prerequisite relationship)."""
    model = load_model()

    # Find both concepts
    concept_key = find_concept(model, args.concept_name)
    related_key = find_concept(model, args.related_concept)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    # Warn if related concept doesn't exist yet
    if not related_key:
        print(f"⚠️  '{args.related_concept}' not tracked yet.")
        print(f"   Link will be created, but you should add it:")
        print(f"   python student.py add \"{args.related_concept}\" 0 low")
        # Use the provided name as-is
        link_name = args.related_concept
    else:
        # Use the exact key from the model
        link_name = related_key

    concept = model["concepts"][concept_key]
    related_list = concept.setdefault('related_concepts', [])

    # Check for duplicates (case-insensitive)
    if any(r.lower() == link_name.lower() for r in related_list):
        print(f"ℹ️  Already linked.")
        return

    # Add the link
    related_list.append(link_name)

    if save_model(model):
        print(f"✅ Linked '{concept_key}' → '{link_name}'")
    else:
        print("❌ Failed to save model")


def cmd_unlink(args):
    """Remove a link between two concepts."""
    model = load_model()

    concept_key = find_concept(model, args.concept_name)

    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return

    concept = model["concepts"][concept_key]
    related_list = concept.get('related_concepts', [])

    # Find the related concept to remove (case-insensitive)
    removed = None
    for rel in related_list:
        if rel.lower() == args.related_concept.lower():
            removed = rel
            break

    if not removed:
        print(f"ℹ️  No link found between '{concept_key}' and '{args.related_concept}'")
        return

    # Remove the link
    related_list.remove(removed)

    if save_model(model):
        print(f"✅ Unlinked '{concept_key}' ✗ '{removed}'")
    else:
        print("❌ Failed to save model")


def cmd_session_end(args):
    """
    Batch operation for session end - update multiple concepts atomically.
    
    Format:
        --update "Concept:mastery:confidence"
        --struggle "Concept:description"
        --breakthrough "Concept:description"
    """
    model = load_model()
    
    changes = []
    errors = []
    
    # Process updates
    if hasattr(args, 'update') and args.update:
        for update_str in args.update:
            try:
                parts = update_str.split(':')
                if len(parts) != 3:
                    errors.append(f"Invalid update format: '{update_str}' (expected 'Concept:mastery:confidence')")
                    continue
                
                concept_name, mastery_str, confidence = parts
                mastery = int(mastery_str)
                
                # Validate
                if not (0 <= mastery <= 100):
                    errors.append(f"Invalid mastery for '{concept_name}': {mastery} (must be 0-100)")
                    continue
                
                if confidence not in ['low', 'medium', 'high']:
                    errors.append(f"Invalid confidence for '{concept_name}': {confidence} (must be low/medium/high)")
                    continue
                
                # Find concept
                concept_key = find_concept(model, concept_name)
                if not concept_key:
                    errors.append(f"Concept '{concept_name}' not found")
                    continue
                
                concept = model["concepts"][concept_key]
                old_mastery = concept.get('mastery', 0)
                old_confidence = concept.get('confidence', 'unknown')
                
                # Apply changes
                concept['mastery'] = mastery
                concept['confidence'] = confidence
                concept['last_reviewed'] = datetime.now().isoformat()
                
                changes.append(f"  ✅ Updated '{concept_key}': {old_mastery}% → {mastery}%, {old_confidence} → {confidence}")
                
            except ValueError:
                errors.append(f"Invalid mastery value in: '{update_str}'")
            except Exception as e:
                errors.append(f"Error processing update '{update_str}': {str(e)}")
    
    # Process struggles
    if hasattr(args, 'struggle') and args.struggle:
        for struggle_str in args.struggle:
            try:
                # Format: "Concept:description"
                if ':' not in struggle_str:
                    errors.append(f"Invalid struggle format: '{struggle_str}' (expected 'Concept:description')")
                    continue
                
                concept_name, description = struggle_str.split(':', 1)
                
                # Find concept
                concept_key = find_concept(model, concept_name)
                if not concept_key:
                    errors.append(f"Concept '{concept_name}' not found")
                    continue
                
                concept = model["concepts"][concept_key]
                
                # Check for duplicate
                struggles = concept.get('struggles', [])
                if description in struggles:
                    changes.append(f"  ℹ️  Struggle already logged for '{concept_key}'")
                    continue
                
                # Add struggle
                concept.setdefault('struggles', []).append(description)
                concept['last_reviewed'] = datetime.now().isoformat()
                
                changes.append(f"  ✅ Added struggle to '{concept_key}': \"{description}\"")
                
            except Exception as e:
                errors.append(f"Error processing struggle '{struggle_str}': {str(e)}")
    
    # Process breakthroughs
    if hasattr(args, 'breakthrough') and args.breakthrough:
        for breakthrough_str in args.breakthrough:
            try:
                # Format: "Concept:description"
                if ':' not in breakthrough_str:
                    errors.append(f"Invalid breakthrough format: '{breakthrough_str}' (expected 'Concept:description')")
                    continue
                
                concept_name, description = breakthrough_str.split(':', 1)
                
                # Find concept
                concept_key = find_concept(model, concept_name)
                if not concept_key:
                    errors.append(f"Concept '{concept_name}' not found")
                    continue
                
                concept = model["concepts"][concept_key]
                
                # Check for duplicate
                breakthroughs = concept.get('breakthroughs', [])
                if description in breakthroughs:
                    changes.append(f"  ℹ️  Breakthrough already logged for '{concept_key}'")
                    continue
                
                # Add breakthrough
                concept.setdefault('breakthroughs', []).append(description)
                concept['last_reviewed'] = datetime.now().isoformat()
                
                changes.append(f"  ✅ Added breakthrough to '{concept_key}': 💡 \"{description}\"")
                
            except Exception as e:
                errors.append(f"Error processing breakthrough '{breakthrough_str}': {str(e)}")
    
    # Report errors
    if errors:
        print("❌ Errors encountered:")
        for error in errors:
            print(f"   {error}")
        print()
    
    # Report changes
    if changes:
        print("📊 Session-End Updates:")
        for change in changes:
            print(change)
        
        # Save model
        if save_model(model):
            print(f"\n✅ All changes saved successfully ({len(changes)} operations)")
        else:
            print("\n❌ Failed to save model - changes may be lost")
    else:
        print("ℹ️  No changes to apply")
        if not errors:
            print("   Use --update, --struggle, or --breakthrough flags")



# PHASE 5: Misconception tracking

def cmd_misconception_add(args):
    """Add a misconception for a concept."""
    model = load_model()
    
    # Verify concept exists
    concept_key = find_concept(model, args.concept_name)
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        print(f"   Add it first: python student.py add \"{args.concept_name}\" 0 low")
        return
    
    # Create misconception entry
    misconception = {
        "concept": concept_key,
        "belief": args.belief,
        "correction": args.correction,
        "date_identified": datetime.now().isoformat(),
        "resolved": False,
        "date_resolved": None
    }
    
    # Check for duplicate (same concept + same belief)
    misconceptions = model.setdefault("misconceptions", [])
    for m in misconceptions:
        if (m["concept"].lower() == concept_key.lower() and 
            m["belief"].lower() == args.belief.lower()):
            print(f"ℹ️  This misconception already logged.")
            return
    
    # Add misconception
    misconceptions.append(misconception)
    
    if save_model(model):
        print(f"✅ Logged misconception for '{concept_key}'")
        print(f"   Belief: \"{args.belief}\"")
        print(f"   Correction: \"{args.correction}\"")
    else:
        print("❌ Failed to save model")


def cmd_misconception_resolve(args):
    """Mark a misconception as resolved."""
    model = load_model()
    
    concept_key = find_concept(model, args.concept_name)
    if not concept_key:
        print(f"❌ Concept '{args.concept_name}' not found.")
        return
    
    # Find unresolved misconceptions for this concept
    misconceptions = model.get("misconceptions", [])
    concept_misconceptions = [
        (i, m) for i, m in enumerate(misconceptions)
        if m["concept"].lower() == concept_key.lower() and not m["resolved"]
    ]
    
    if not concept_misconceptions:
        print(f"ℹ️  No unresolved misconceptions for '{concept_key}'")
        return
    
    # Validate index
    if args.index >= len(concept_misconceptions):
        print(f"❌ Index {args.index} out of range (0-{len(concept_misconceptions)-1})")
        print(f"   Run: python student.py misconception list \"{concept_key}\" --unresolved")
        return
    
    # Get the actual index in the misconceptions array
    actual_index, misconception = concept_misconceptions[args.index]
    
    # Mark as resolved
    misconceptions[actual_index]["resolved"] = True
    misconceptions[actual_index]["date_resolved"] = datetime.now().isoformat()
    
    if save_model(model):
        print(f"✅ Resolved misconception for '{concept_key}'")
        print(f"   \"{misconception['belief']}\"")
    else:
        print("❌ Failed to save model")


def cmd_misconception_list(args):
    """List all misconceptions, optionally filtered."""
    model = load_model()
    
    misconceptions = model.get("misconceptions", [])
    
    if not misconceptions:
        print("📚 No misconceptions tracked yet.")
        print("   Add one with: python student.py misconception add \"Concept\" --belief \"...\" --correction \"...\"")
        return
    
    # Filter by concept if specified
    display_concept = None
    if hasattr(args, 'concept_name') and args.concept_name:
        concept_key = find_concept(model, args.concept_name)
        if not concept_key:
            print(f"❌ Concept '{args.concept_name}' not found.")
            return
        misconceptions = [m for m in misconceptions if m["concept"].lower() == concept_key.lower()]
        display_concept = concept_key
    
    # Filter by resolved status if specified
    if hasattr(args, 'resolved_only') and args.resolved_only:
        misconceptions = [m for m in misconceptions if m["resolved"]]
    elif hasattr(args, 'unresolved_only') and args.unresolved_only:
        misconceptions = [m for m in misconceptions if not m["resolved"]]
    
    # Header
    if display_concept:
        status_filter = ""
        if hasattr(args, 'resolved_only') and args.resolved_only:
            status_filter = " (resolved only)"
        elif hasattr(args, 'unresolved_only') and args.unresolved_only:
            status_filter = " (unresolved only)"
        print(f"🐛 Misconceptions for '{display_concept}'{status_filter}:\n")
    else:
        print(f"🐛 All Misconceptions ({len(misconceptions)} total):\n")
    
    if not misconceptions:
        print("   None found.")
        return
    
    # Group by concept
    by_concept = {}
    for m in misconceptions:
        concept = m["concept"]
        by_concept.setdefault(concept, []).append(m)
    
    # Display grouped by concept
    for concept, items in sorted(by_concept.items()):
        print(f"📌 {concept}:")
        
        # Get unresolved items for this concept (for indexing)
        unresolved_items = [m for m in items if not m["resolved"]]
        
        for i, m in enumerate(items):
            status = "✅ Resolved" if m["resolved"] else "⚠️  Active"
            date = m["date_identified"].split('T')[0]
            
            # Show index only for unresolved items
            if not m["resolved"]:
                index = unresolved_items.index(m)
                print(f"   [{index}] {status}")
            else:
                print(f"       {status}")
            
            print(f"       Belief: \"{m['belief']}\"")
            print(f"       Correction: \"{m['correction']}\"")
            print(f"       Identified: {date}")
            
            if m["resolved"] and m["date_resolved"]:
                resolved_date = m["date_resolved"].split('T')[0]
                print(f"       Resolved: {resolved_date}")
            print()


# =============================================================================
# MAIN CLI ENTRY POINT
# =============================================================================

def main():
    """Main CLI entry point."""
    parser = argparse.ArgumentParser(
        description='Student Model CLI - Track conceptual knowledge mastery',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # PHASE 1 COMMANDS

    # Init command
    parser_init = subparsers.add_parser('init', help='Initialize a new student model')
    parser_init.add_argument('--profile', type=str, default='',
                            help='Student profile description')

    # Info command
    parser_info = subparsers.add_parser('info', help='Show model information')

    # PHASE 2 COMMANDS

    # List command
    parser_list = subparsers.add_parser('list', help='List all tracked concepts')

    # Show command
    parser_show = subparsers.add_parser('show', help='Show detailed concept information')
    parser_show.add_argument('concept_name', type=str, help='Name of the concept to show')

    # Related command
    parser_related = subparsers.add_parser('related', help='Show related concepts')
    parser_related.add_argument('concept_name', type=str, help='Name of the concept')

    # PHASE 3 COMMANDS

    # Add command
    parser_add = subparsers.add_parser('add', help='Add a new concept')
    parser_add.add_argument('concept_name', type=str, help='Name of the concept')
    parser_add.add_argument('mastery', type=int, help='Mastery level (0-100)')
    parser_add.add_argument('confidence', type=str,
                           choices=['low', 'medium', 'high'],
                           help='Confidence level')
    parser_add.add_argument('--related', type=str, default='',
                           help='Comma-separated list of related concepts')

    # Update command
    parser_update = subparsers.add_parser('update', help='Update concept mastery/confidence')
    parser_update.add_argument('concept_name', type=str, help='Name of the concept')
    parser_update.add_argument('--mastery', type=int, default=None,
                              help='New mastery level (0-100)')
    parser_update.add_argument('--confidence', type=str,
                              choices=['low', 'medium', 'high'],
                              default=None,
                              help='New confidence level')

    # Struggle command
    parser_struggle = subparsers.add_parser('struggle', help='Log a struggle with a concept')
    parser_struggle.add_argument('concept_name', type=str, help='Name of the concept')
    parser_struggle.add_argument('description', type=str, help='Description of the struggle')

    # Breakthrough command
    parser_breakthrough = subparsers.add_parser('breakthrough', help='Log a breakthrough')
    parser_breakthrough.add_argument('concept_name', type=str, help='Name of the concept')
    parser_breakthrough.add_argument('description', type=str, help='Description of the breakthrough')

    # Link command
    parser_link = subparsers.add_parser('link', help='Link two concepts (prerequisite)')
    parser_link.add_argument('concept_name', type=str, help='Main concept')
    parser_link.add_argument('related_concept', type=str, help='Related/prerequisite concept')

    # Unlink command
    parser_unlink = subparsers.add_parser('unlink', help='Remove link between concepts')
    parser_unlink.add_argument('concept_name', type=str, help='Main concept')
    parser_unlink.add_argument('related_concept', type=str, help='Related concept to unlink')

    # Session-end command (Phase 3.2)
    parser_session_end = subparsers.add_parser(
        'session-end',
        help='Batch update multiple operations at session end'
    )
    parser_session_end.add_argument(
        '--update',
        action='append',
        help='Update concept: "Concept:mastery:confidence" (can specify multiple times)'
    )
    parser_session_end.add_argument(
        '--struggle',
        action='append',
        help='Add struggle: "Concept:description" (can specify multiple times)'
    )
    parser_session_end.add_argument(
        '--breakthrough',
        action='append',
        help='Add breakthrough: "Concept:description" (can specify multiple times)'
    )

    # PHASE 5 COMMANDS

    # Misconception commands (Phase 5.2)
    parser_misconception = subparsers.add_parser(
        'misconception',
        help='Track and manage misconceptions'
    )
    
    misconception_subparsers = parser_misconception.add_subparsers(
        dest='misconception_command',
        help='Misconception operations'
    )
    
    # misconception add
    parser_misc_add = misconception_subparsers.add_parser(
        'add',
        help='Add a misconception'
    )
    parser_misc_add.add_argument('concept_name', type=str, help='Concept name')
    parser_misc_add.add_argument('--belief', type=str, required=True,
                                help='The incorrect belief')
    parser_misc_add.add_argument('--correction', type=str, required=True,
                                help='The correct understanding')
    
    # misconception resolve
    parser_misc_resolve = misconception_subparsers.add_parser(
        'resolve',
        help='Mark a misconception as resolved'
    )
    parser_misc_resolve.add_argument('concept_name', type=str, help='Concept name')
    parser_misc_resolve.add_argument('index', type=int,
                                    help='Index of misconception to resolve (from list)')
    
    # misconception list
    parser_misc_list = misconception_subparsers.add_parser(
        'list',
        help='List misconceptions'
    )
    parser_misc_list.add_argument('concept_name', type=str, nargs='?', default=None,
                                 help='Filter by concept (optional)')
    parser_misc_list.add_argument('--resolved', dest='resolved_only',
                                 action='store_true',
                                 help='Show only resolved misconceptions')
    parser_misc_list.add_argument('--unresolved', dest='unresolved_only',
                                 action='store_true',
                                 help='Show only unresolved misconceptions')

    # Parse arguments
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Route to command handlers
    if args.command == 'init':
        cmd_init(args)
    elif args.command == 'info':
        cmd_info(args)
    elif args.command == 'list':
        cmd_list(args)
    elif args.command == 'show':
        cmd_show(args)
    elif args.command == 'related':
        cmd_related(args)
    elif args.command == 'add':
        cmd_add(args)
    elif args.command == 'update':
        cmd_update(args)
    elif args.command == 'struggle':
        cmd_struggle(args)
    elif args.command == 'breakthrough':
        cmd_breakthrough(args)
    elif args.command == 'link':
        cmd_link(args)
    elif args.command == 'unlink':
        cmd_unlink(args)
    elif args.command == 'session-end':
        cmd_session_end(args)
    elif args.command == 'misconception':
        if not args.misconception_command:
            print("❌ Please specify: add, resolve, or list")
            print("   Usage: python student.py misconception {add|resolve|list}")
            return
        if args.misconception_command == 'add':
            cmd_misconception_add(args)
        elif args.misconception_command == 'resolve':
            cmd_misconception_resolve(args)
        elif args.misconception_command == 'list':
            cmd_misconception_list(args)

if __name__ == '__main__':
    main()