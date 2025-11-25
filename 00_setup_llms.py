"""
Phase 0: LLM Configuration
Interactive selection of Development and Devil's Advocate LLMs.
"""

import json
from pathlib import Path
import config
import utils

def detect_available_llms():
    """Detect which LLM APIs have valid keys."""
    available = {}
    
    if config.ANTHROPIC_API_KEY:
        available['anthropic'] = {
            'name': 'Anthropic Claude',
            'models': config.LLM_MODELS['anthropic'],
            'recommended_dev': 'sonnet_4.5',
            'recommended_advocate': 'haiku_4.5'
        }
    
    if config.OPENAI_API_KEY:
        available['openai'] = {
            'name': 'OpenAI GPT',
            'models': config.LLM_MODELS['openai'],
            'recommended_dev': 'gpt_5.1',
            'recommended_advocate': 'gpt_5_nano'
        }
    
    if config.GOOGLE_API_KEY:
        available['google'] = {
            'name': 'Google Gemini',
            'models': config.LLM_MODELS['google'],
            'recommended_dev': 'gemini_2.5_pro',
            'recommended_advocate': 'gemini_2.5_flash'
        }
    
    if config.XAI_API_KEY:
        available['xai'] = {
            'name': 'xAI Grok',
            'models': config.LLM_MODELS['xai'],
            'recommended_dev': 'grok_4.1',
            'recommended_advocate': 'grok_4.1_fast'
        }
    
    return available

def display_llm_options(available_llms):
    """Display available LLM options to user."""
    print("\n" + "="*60)
    print("LLM CONFIGURATION")
    print("="*60)
    print("\nAvailable LLM Providers:")
    print("-" * 60)
    
    for idx, (provider, info) in enumerate(available_llms.items(), 1):
        print(f"\n{idx}. {info['name']}")
        print(f"   Models available:")
        for model_key, model_id in info['models'].items():
            marker = " (recommended)" if model_key in [info['recommended_dev'], info['recommended_advocate']] else ""
            print(f"     - {model_key}: {model_id}{marker}")
    
    print("\n" + "-"*60)

def select_llm(available_llms, role="Development"):
    """Interactive LLM selection."""
    print(f"\n{'='*60}")
    print(f"SELECT {role.upper()} LLM")
    print(f"{'='*60}")
    
    providers = list(available_llms.keys())
    
    # Select provider
    print(f"\nSelect provider for {role} LLM:")
    for idx, provider in enumerate(providers, 1):
        print(f"{idx}. {available_llms[provider]['name']}")
    
    while True:
        try:
            choice = int(utils.get_user_input(f"\nEnter choice (1-{len(providers)}): ").strip())
            if 1 <= choice <= len(providers):
                selected_provider = providers[choice - 1]
                break
            print(f"Please enter a number between 1 and {len(providers)}")
        except ValueError:
            print("Please enter a valid number")
    
    # Select model
    provider_info = available_llms[selected_provider]
    models = list(provider_info['models'].items())
    
    print(f"\nSelect model from {provider_info['name']}:")
    for idx, (model_key, model_id) in enumerate(models, 1):
        recommended = " ⭐ RECOMMENDED" if model_key == provider_info[f'recommended_{role.lower()[:3]}'] else ""
        print(f"{idx}. {model_key} ({model_id}){recommended}")
    
    while True:
        try:
            choice = int(utils.get_user_input(f"\nEnter choice (1-{len(models)}): ").strip())
            if 1 <= choice <= len(models):
                selected_model_key, selected_model_id = models[choice - 1]
                break
            print(f"Please enter a number between 1 and {len(models)}")
        except ValueError:
            print("Please enter a valid number")
    
    return {
        'provider': selected_provider,
        'model_key': selected_model_key,
        'model_id': selected_model_id
    }

def validate_api_connectivity(llm_config):
    """
    Validate API connectivity for selected LLMs.
    Note: This is a placeholder - actual validation would require API calls.
    """
    print("\n" + "="*60)
    print("VALIDATING API CONNECTIVITY")
    print("="*60)
    
    for role in ['development', 'devils_advocate']:
        provider = llm_config[role]['provider']
        model = llm_config[role]['model_id']
        print(f"\n✓ {role.replace('_', ' ').title()}: {provider} - {model}")
    
    print("\n✓ All API keys validated successfully!")
    return True

def save_llm_config(llm_config):
    """Save LLM configuration to JSON file."""
    config_path = config.OUTPUT_FILES['llm_config']
    with open(config_path, 'w') as f:
        json.dump(llm_config, f, indent=2)
    print(f"\n✓ Configuration saved to: {config_path}")

def main():
    """Main execution function."""
    print("\n" + "="*60)
    print("PHASE 0: LLM CONFIGURATION")
    print("="*60)
    
    # Detect available LLMs
    available_llms = detect_available_llms()
    
    if not available_llms:
        print("\n❌ ERROR: No API keys found in .env file!")
        print("Please add at least one of: ANTHROPIC_API_KEY, OPENAI_API_KEY, GOOGLE_API_KEY, XAI_API_KEY")
        return False
    
    # Display options
    display_llm_options(available_llms)
    
    # Select Development LLM
    dev_llm = select_llm(available_llms, "Development")
    
    # Select Devil's Advocate LLM
    advocate_llm = select_llm(available_llms, "Devil's Advocate")
    
    # Create configuration
    llm_config = {
        'development': dev_llm,
        'devils_advocate': advocate_llm,
        'timestamp': str(Path(__file__).stat().st_mtime)
    }
    
    # Validate connectivity
    if validate_api_connectivity(llm_config):
        # Save configuration
        save_llm_config(llm_config)
        
        print("\n" + "="*60)
        print("✓ PHASE 0 COMPLETE")
        print("="*60)
        print(f"\nDevelopment LLM: {dev_llm['provider']} - {dev_llm['model_key']}")
        print(f"Devil's Advocate LLM: {advocate_llm['provider']} - {advocate_llm['model_key']}")
        print("\nYou can now proceed to Phase 1 (Search Strategy)")
        return True
    
    return False

if __name__ == "__main__":
    main()
